import functools

import paddle
import paddle.fluid as fluid

from paddle_tokenizer.data_reader import generator_fn

dict_size = 128003
EMBED_SIZE = 128
hidden_dim = 64

if __name__ == "__main__":
    words = fluid.layers.data(name="words", shape=[1], dtype="int64", lod_level=1)
    tags = fluid.layers.data(name="tags", shape=[1], dtype="int64", lod_level=1)

    embed_char = fluid.layers.embedding(
        input=words, size=[dict_size, EMBED_SIZE], dtype="float32"
    )

    place = fluid.CPUPlace()

    dataset_func = functools.partial(
        generator_fn, "data/train.txt", "data/unicode_char_list.txt", "data/tags.txt"
    )

    train_reader = paddle.batch(
        paddle.reader.shuffle(dataset_func, buf_size=500), batch_size=256
    )

    forward_hidden_state, _ = fluid.layers.dynamic_lstm(
        input=embed_char,
        size=EMBED_SIZE,
        candidate_activation="relu",
        gate_activation="sigmoid",
        cell_activation="sigmoid",
    )

    backward_hidden_state, _ = fluid.layers.dynamic_lstm(
        input=embed_char,
        size=EMBED_SIZE,
        candidate_activation="relu",
        gate_activation="sigmoid",
        cell_activation="sigmoid",
        is_reverse=True,
    )

    hidden_state = fluid.layers.concat([forward_hidden_state, backward_hidden_state], 1)

    feature = fluid.layers.dropout(hidden_state, 0.1)

    score = fluid.layers.fc(feature, 4)

    crf_cost = fluid.layers.linear_chain_crf(
        input=score, label=tags, param_attr=fluid.ParamAttr(name="crfw")
    )

    avg_cost = fluid.layers.mean(crf_cost)

    crf_decode = fluid.layers.crf_decoding(
        input=score, param_attr=fluid.ParamAttr(name="crfw")
    )

    sgd_optimizer = fluid.optimizer.AdamOptimizer(learning_rate=0.01)

    sgd_optimizer.minimize(avg_cost)

    feeder = fluid.DataFeeder(place=place, feed_list=[words, tags])
    exe = fluid.Executor(place)

    exe.run(fluid.default_startup_program())

    save_dirname = "test.inference.model"
    main_program = fluid.default_main_program()

    PASS_NUM = 20
    for pass_id in range(PASS_NUM):
        print(">>> pass_id: {}".format(pass_id))
        for data in train_reader():
            feed = feeder.feed(data)

            avg_loss_value, = exe.run(
                main_program, feed=feed, fetch_list=[avg_cost], return_numpy=True
            )
            print(avg_loss_value[0])

    if save_dirname is not None:
        fluid.io.save_inference_model(save_dirname, ["words"], [crf_decode], exe)
