from PIL import Image
import sys

R = 0
G = 1
B = 2   

def sqr(a):
    return a*a

def computeDistance(color_1, color_2):
    return sqr(color_1[R]-color_2[R]) + sqr(color_1[G] - color_2[G]) + sqr(color_1[B] - color_2[B])

def findNearestColor(input_color, current_color):
    min_distance = 1000000
    index = 0
    for a_color in input_color:
        index += 1
        if computeDistance(a_color, current_color) < min_distance:
            min_distance = computeDistance(a_color, current_color)
            min_distance_color = a_color

    return min_distance_color

def blurImage(im, input_color, x_num, y_num):
    width = im.size[0]
    length = im.size[1]
    print length, width

    #box = (0,0, 1000, 1000)
    #region = im.crop(box)
    #region.show()

    px = im.load()
    #print px[0,0]

    output_image = Image.new("RGB", (x_num, y_num))
    output_pixel = output_image.load()

    for x_n in range(x_num):
        if width % x_num == 0 or x_num == 29:
            x_unit = width/x_num
        else:
            x_unit = width/x_num + 1
        x_start = x_n * (x_unit)
        x_end = min((x_n+1)*(x_unit), width)
        for y_n in range(y_num):
            if width % y_num == 0 or y_num == 29:
                y_unit = width/y_num
            else:
                y_unit = width/y_num + 1
            y_start = y_n * (y_unit)
            y_end = min((y_n+1)*(y_unit), length)
            #print x_start, x_end, y_start, y_end
            color_total = {}
            color_total[R] = 0
            color_total[G] = 0
            color_total[B] = 0
            for x in range(x_start, x_end):
                for y in range(y_start, y_end):
                    color_total[R] += px[x,y][R]
                    color_total[G] += px[x,y][G]
                    color_total[B] += px[x,y][B]
            
            if (x_start >= x_end or y_start >= y_end):
                new_r = 255
                new_g = 255
                new_b = 255
            else:
                new_r = color_total[R] / ((x_end-x_start) * (y_end - y_start))
                new_g = color_total[G] / ((x_end-x_start) * (y_end - y_start))
                new_b = color_total[B] / ((x_end-x_start) * (y_end - y_start))

            output_pixel[x_n, y_n] = findNearestColor(input_color, (new_r, new_g, new_b))

        print 'done', x_n, y_n

    return output_image

def main():

    x_num = 29
    y_num = 29

    remove_list = []
    #remove_list = ['purple']

    input_color = []
    fin = open('input_color','r')
    for line in fin:
        items = line.strip().split()
        if items[3] not in remove_list:
            input_color.append((int(items[0]), int(items[1]), int(items[2])))
    fin.close()

    im = Image.open(sys.argv[1])
    #im.show()
    #out = im.point(lambda i: i * 1.7)
    #im = Image.open('IMG_0242.JPG')
    #print(im.format, im.size, im.mode)
    #exit()

    out = blurImage(im, input_color, 500, 500)
    out.show()
    out = blurImage(out, input_color, 100, 100)
    out.show()
    out = blurImage(out, input_color, 29, 29)
    out.show()

    #blurImage(im, input_color, 50, 50).show()

    #output_image.show()


if __name__ == '__main__':
    main()
