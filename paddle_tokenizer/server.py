import numpy as np
import paddle.fluid as fluid
from tokenizer_tools.tagset.BMES import BMESEncoderDecoder

from paddle_tokenizer.data_reader import read_vocabulary

exe = fluid.Executor(fluid.CPUPlace())
path = "./test.inference.model"


[inference_program, feed_target_names, fetch_targets] = fluid.io.load_inference_model(
    dirname=path, executor=exe
)

place = fluid.CPUPlace()

decoder = BMESEncoderDecoder()

vocabulary = read_vocabulary("data/unicode_char_list.txt")
reverse_vocabulary = {v: k for k, v in vocabulary.items()}

tag = read_vocabulary("data/tags.txt")
reverse_tag = {v: k for k, v in tag.items()}


def infer(data):
    word = fluid.create_lod_tensor([data], [[len(data)]], place)

    results, = exe.run(
        inference_program,
        feed={feed_target_names[0]: word},
        fetch_list=fetch_targets,
        return_numpy=False,
    )

    raw_data = np.array(results)
    result = raw_data.reshape([-1])
    print(result)
    return result.tolist()


def server(input_text):
    data = [vocabulary[i] for i in input_text]
    result = infer(data)

    output_tag = [reverse_tag[i] for i in result]

    result = decoder.decode_char_tag_pair(list(zip(input_text, output_tag)))
    return result


if __name__ == "__main__":
    result = server("王小明在北京的清华大学读书。")
    print(result)
