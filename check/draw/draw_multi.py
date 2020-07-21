import pygal
import random


# input: dictS of suspect index of MULTIPLE Questions
# file_dicts:
# {
#     Question_name_0: {
#         "111.py": 0.111,
#         "222.py": 0.222,
#     },
#     Question_name_1: {
#         ....
#     },
#     .....
# }
def draw_multi(file_dicts):
    # 1. draw a solid gauge
    gauge = pygal.SolidGauge(half_pie=True, inner_radius=.7)
    gauge.value_formatter = lambda x: '{:.10g}%'.format(x)
    gauge.title = "Proportion of suspected files in multiple questions".title()

    for question_name in file_dicts.keys():
        file_index_dict = file_dicts[question_name]
        problem_files_num = 0
        for key in file_index_dict.keys():
            if file_index_dict[key] > 0.5:
                problem_files_num += 1
        gauge.add(question_name, [{'value': 100 * round(problem_files_num / len(file_index_dict), 2), 'max_value': 100}])

    gauge.render_to_file("../pics/dataGaugeMulti.svg")

    # 2. draw a Pyramid
    args = []
    types = []
    for question_name in file_dicts.keys():
        file_index_dict = file_dicts[question_name]
        arg = [0 for x in range(101)]  # 0 ~ 100
        for ele in file_index_dict.values():
            arg[int(ele * 100)] += 1
        args.append(tuple(arg))
        types.append(question_name)

    pyramid = pygal.Pyramid(human_readable=True, legend_at_bottom=True)
    pyramid.title = "Question Suspected Files Distribution"
    pyramid.x_labels = map(lambda x: str(x / 100) if x % 10 == 0 else "", range(101))
    for type, arg in zip(types, args):
        pyramid.add(type, arg)

    pyramid.render_to_file("../pics/dataPyramidMulti.svg")


def random_dict():
    x_dict = {}
    i = 0
    while i < 739:
        a_double = random.randint(0, 9) / 10 + random.randint(0, 9) / 100 + random.randint(0, 9) / 1000
        x_dict[str(i)] = a_double
        i += 1
    return x_dict


def test():
    file_dicts = {}
    count = 0
    while count < 6:
        name = "Question NO." + str(count)
        file_dicts[name] = random_dict()
        count += 1

    draw_multi(file_dicts)


if __name__=="__main__":
    test()