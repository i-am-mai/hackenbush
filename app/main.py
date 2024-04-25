from fractions import Fraction
from math import floor
import bokeh
from bokeh.io import show
from bokeh.models import Slider, CustomJS, ColumnDataSource, Segment, Circle, Range1d
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column

def numbers_born_by(day: int) -> list[Fraction]:
    numbers: list[Fraction] = []
    number_day: list[list[Fraction]] = []
    numbers.append(Fraction(0, 1))
    number_day.append([Fraction(0, 1)])

    for i in range(day):
        new_numbers: list[Fraction] = []
        for i in range(0, len(numbers) - 1):
            new_numbers.append((numbers[i] + numbers[i + 1]) / 2)
        new_numbers.insert(0, numbers[0] - 1)
        new_numbers.append(numbers[-1] + 1)

        number_day.append(new_numbers)

        i = 0
        j = 0
        while j < len(new_numbers):
            numbers.insert(i, new_numbers[j])
            i += 2
            j += 1
    return numbers, number_day

def number_to_string(number: Fraction) -> str:
    output: str = ""
    if int(number) == number:
        if number > 0: return 'L' * int(abs(number))
        else: return 'R' * int(abs(number))

    if abs(number) > 1:
        if number > 0:
            output += 'L' * floor(abs(number))
            number -= floor(abs(number))
        else:
            output += 'R' * floor(abs(number))
            number += floor(abs(number))
         
    if number > 0:
        output += 'LR'
        while number != 0:
            number *= 2
            bit = floor(number)
            if bit == 1:
                output += 'L' 
            else:
                output += 'R'
            number -= bit
    elif number < 0:
        output += 'RL'
        number = abs(number)
        while number != 0:
            number *= 2
            bit = floor(number)
            if bit == 1:
                output += 'R' 
            else:
                output += 'L'
            number -= bit

    return output[:-1]

# Change this if you want to see more/fewer days
day_limit = 10

numbers, numbers_days = numbers_born_by(day_limit)
strings = [[number_to_string(number) for number in day] for day in numbers_days]
numbers_days_float = [[float(number) for number in day] for day in numbers_days]

def generate_lines(day):
    blue_x = []
    blue_y0 = []
    blue_y1 = []

    red_x = []
    red_y0 = []
    red_y1 = []
    for i in range(day + 1):
        for j in range(len(numbers_days[i])):
            for k, c in enumerate(strings[i][j]):
                if c == 'L':
                    blue_x.append(float(numbers_days[i][j]))
                    blue_y0.append(k)
                    blue_y1.append(k + 1)
                elif c == 'R':
                    red_x.append(float(numbers_days[i][j]))
                    red_y0.append(k)
                    red_y1.append(k + 1)
    return blue_x, blue_y0, blue_y1, red_x, red_y0, red_y1

blue_x, blue_y0, blue_y1, red_x, red_y0, red_y1 = generate_lines(1)

source = ColumnDataSource(data={
        'bx': blue_x,
        'by': blue_y0,
        'by1': blue_y1,
        'rx': red_x,
        'ry':red_y0,
        'ry1':red_y1
}
)

# Display the plot
slider = Slider(start=0, end=day_limit, value=1, step=1, title="Day", name="slider")
p = figure(width=1200, height=500, name="plot")
p.yaxis.visible = False
p.grid.visible = False

p.x_range = Range1d(-11, 11)
p.y_range = Range1d(0, 11)

blue_lines = Segment(x0="bx", y0="by", x1="bx",
          y1="by1", line_color="blue", line_width=2)

red_lines = Segment(x0="rx", y0="ry", x1="rx",
          y1="ry1", line_color="red", line_width=2)

blue_circles = Circle(x="bx", y="by1", radius=0.04, fill_color="blue", line_color="blue")
red_circles = Circle(x="rx", y="ry1", radius=0.04, fill_color="red", line_color="red")

p.add_glyph(source, blue_lines)
p.add_glyph(source, red_lines)
p.add_glyph(source, blue_circles)
p.add_glyph(source, red_circles)

slider.js_on_change('value', CustomJS(args=dict(source=source, numbers_days=numbers_days_float, strings=strings), code="""
    const day = cb_obj.value;
                                   
    let blue_x = []
    let blue_y0 = []
    let blue_y1 = []

    let red_x = []
    let red_y0 = []
    let red_y1 = []

    for (let i = 0; i <= day; i++) {
        for (let j = 0; j < numbers_days[i].length; j++) {
            [...strings[i][j]].forEach((c, k) => {
                if (c === 'L') {
                    blue_x.push(numbers_days[i][j])
                    blue_y0.push(k)
                    blue_y1.push(k + 1)
                }
                else if (c === 'R') {
                    red_x.push(numbers_days[i][j])
                    red_y0.push(k)
                    red_y1.push(k + 1)
                }
            });
        }
    }
                                                                         
    source.data.bx = blue_x
    source.data.by = blue_y0
    source.data.by1 = blue_y1
    source.data.rx = red_x
    source.data.ry = red_y0
    source.data.ry1 = red_y1
                                      
    source.change.emit();
"""))

layout = column(slider, p)

curdoc().add_root(layout)