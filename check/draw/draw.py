import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS
import random


def count_range_num(a_list, start, end):
    count = 0
    for ele in a_list:
        if ele >= start and ele < end:
            count += 1
        elif end == 1 and ele == 1:
            count += 1
    return count


def draw(file_index_dict, q_id):
    # 1. use pygal to draw a bar of suspect_index (decrease)
    sorted_items = sorted(file_index_dict.items(), key=lambda x: x[1], reverse=True)

    x_ax, y_ax = [], []
    for item in sorted_items:
        x_ax.append(item[0])
        y_ax.append(item[1])

    # visualize
    my_style = LS("#006670", base_style=LCS)

    my_config = pygal.Config()
    my_config.x_label_rotation = 45
    my_config.show_legend = False
    my_config.title_font_size = 24
    my_config.major_label_font_size = 18  # OF NO USE?
    my_config.label_font_size = 14
    my_config.truncate_label = 15
    my_config.show_y_guides = True
    my_config.width = 1000

    chart = pygal.Bar(my_config, style=my_style)
    chart.title = "Most-suspected Files in Question NO." + str(q_id)
    chart.x_labels = x_ax

    chart.add("Suspect Index:", y_ax)
    # chart.render_to_file("C:\\Users\\11381\\Desktop\\dataBar.svg")
    chart.render_to_file("./pics/dataBar.svg")

    # 2. draw a pie of proportion of suspect-index at all levels
    pie = pygal.Pie(inner_radius=.4)
    pie.title = "Proportion of Suspect-Index at all levels (in %)"

    n_00_01 = count_range_num(y_ax, 0, 0.1)
    n_01_03 = count_range_num(y_ax, 0.1, 0.3)
    n_03_05 = count_range_num(y_ax, 0.3, 0.5)
    n_05_07 = count_range_num(y_ax, 0.5, 0.7)
    n_07_08 = count_range_num(y_ax, 0.7, 0.8)
    n_08_09 = count_range_num(y_ax, 0.8, 0.9)
    n_09_10 = count_range_num(y_ax, 0.9, 1)
    n_total = len(y_ax)

    pie.add("0.0 ~ 0.1", round(n_00_01 / n_total * 100, 2))
    pie.add("0.1 ~ 0.3", round(n_01_03 / n_total * 100,2))
    pie.add("0.3 ~ 0.5", round(n_03_05 / n_total * 100, 2))
    pie.add("0.5 ~ 0.7", round(n_05_07 / n_total * 100, 2))
    pie.add("0.7 ~ 0.8", round(n_07_08 / n_total * 100, 2))
    pie.add("0.8 ~ 0.9", round(n_08_09 / n_total * 100, 2))
    pie.add("0.9 ~ 1.0", round(n_09_10 / n_total * 100, 2))

    # pie.render_to_file("C:\\Users\\11381\\Desktop\\dataPie.svg")
    pie.render_to_file("./pics/dataPie.svg")

if __name__ == "__main__":
    x_dict = {}
    i = 0
    while i < 30:
        a_double = random.randint(0, 9) / 10 + random.randint(0, 9) / 100 + random.randint(0, 9) / 1000
        x_dict[str(i)] = a_double
        i += 1
    draw(x_dict, 2133)
