# manim external_merge_sort.py -p  
# manim manimtest.py -p  
from manim import *
import random
import colorsys
import numpy as np
import imageio
import os

#animation_generation = True


array_x8  = [600, 300, 400, 500, 200, 800, 100, 700]
array_x10 = [900, 600, 500, 300, 200, 400,   0, 800, 100, 700]
array_x12 = [random.randint(0, 999) for _ in range(12)]
array_x15 = [624, 446, 385, 524, 610, 421, 281,  41, 
             660, 253,  68, 707, 444,  23, 426]
array_x16 = [124, 746, 885, 924, 610, 421, 281,  41, 
             660, 253,  68, 707, 444,  23, 426, 560]

array_x20       = [370, 996, 420, 280, 861, 162, 836,   8, 606, 489, 
              80, 340, 153, 501, 191, 164, 152, 162, 579, 744]
array_x20_best  = [ 990, 910, 850, 790, 710, 670, 670, 580, 530, 480, 
                    420, 370, 330, 280, 210, 180, 122,  92,  49,   4]
array_x20_worst = [   1,  52, 113, 184, 204, 264, 300, 380, 430, 480, 
                    520, 580, 630, 693, 710, 780, 832, 892, 949, 999]
array_x30 = [ 370, 996, 420, 280, 861, 162, 836,  38, 648, 489, 
              80, 340, 153, 501, 191, 164, 152, 162, 579, 744,
             900, 600, 500, 300, 200, 400,   0, 800, 100, 700]

array_x64  = [   135, 137, 492,  92, 172, 718, 949, 541, 304, 937, 
                 47, 659, 352, 124, 324, 857, 399, 688,  51, 734, 
                 26, 861, 491, 193, 461, 733, 583, 964, 731, 603, 
                864, 858, 762, 176, 169, 859, 802, 912, 476, 925, 
                210, 394, 425, 300, 258, 317,  15, 268, 675,  18, 
                220, 589, 177, 194,  61, 504, 332, 367,  41,  13, 
                 59, 419, 153, 676]
'''
 135, 137, 492,  92, 172, 718, 949, 541, 304, 937,  47, 659, 352, 124, 324, 857, 
 399, 688,  51, 734,  26, 861, 491, 193, 461, 733, 583, 964, 731, 603, 864, 858, 
 762, 176, 169, 859, 802, 912, 476, 925, 210, 394, 425, 300, 258, 317,  15, 268, 
 675,  18, 220, 589, 177, 194,  61, 504, 332, 367,  41,  13,  59, 419, 153, 676]
'''
array_x128 = [  195, 594, 239, 251, 350, 486, 366, 266, 795, 873, 
                356, 805, 614, 405, 857, 617, 897, 852, 359, 445, 
                727, 485, 449, 306, 942, 158, 903, 296, 497, 584, 
                427,  99, 869, 773, 583, 362, 810, 678, 373, 524,
                190,  51, 595, 489, 586, 447, 844, 676, 284, 791, 
                852, 923, 128, 757, 143, 624, 387, 420, 572, 684, 
                172, 854, 125, 374, 516, 119, 881, 393, 674,  40, 
                226,  32,   9, 594, 228, 329, 878, 153, 390, 774,
                756, 940, 729, 398, 449, 704, 349, 842, 188, 325,
                376, 193, 902, 659, 774, 722, 786, 287, 818, 298, 
                346, 590, 910, 700,  16, 837, 290, 932, 422, 430,
                359,  21, 898, 668, 653, 506, 209, 829, 570, 655,
                250, 303, 332,  98, 447, 426, 921, 103]

stores_value = array_x30

def num_to_color(num, type = 'pure'):
    pure_color  =   rgb_to_color(np.array(colorsys.hsv_to_rgb(num/999, 1, 1)))
    dark_color  =   rgb_to_color(np.array(colorsys.hsv_to_rgb(num/999, 1, 0.5)))
    light_color =   rgb_to_color(np.array(colorsys.hsv_to_rgb(num/999, 0.5, 1)))
    grey_color =   rgb_to_color(np.array(colorsys.hsv_to_rgb(num/999, 0.5, 0.5)))
    if type == 'pure':
        return pure_color
    elif type == 'dark':
        return dark_color
    elif type == 'light':
        return light_color
    elif type == 'grey':
        return grey_color
    else:
        return pure_color

                       

class Bubbling(Scene):
    def construct(self):
        plane = NumberPlane().set_z_index(-21)
        planebg = Rectangle(width = 20, height = 10, color=BLACK, fill_opacity=0.8).set_z_index(-20)
        self.add(plane,planebg)

        animation_generation = False
        animation_generation = True
        animation_generation = False
        
        #定义storage的表现形式
        storage_size = 0.4
        storage_buff = 0.1
        pointer_size = 0.4
        storage_distance = storage_buff + storage_size
        square = Square(side_length = storage_size, stroke_width = 2, fill_opacity = 1)
        mobpointer = Vector(UP * pointer_size, stroke_width = 5, tip_length = 1)
        boxpointer = Square(side_length = storage_size + storage_buff/2, stroke_width = 5, fill_opacity = 0)

        #内存区域
        memory_capacity = 18
        memory_length = 0
        memory_spare = memory_capacity - memory_length
        memorys = VGroup()
        for i in range(memory_capacity):
            sqr = square.copy().set_fill(color = DARK_GREY).set_stroke(color = LIGHT_GREY)
            num = Text('', font="Times New Roman", font_size=32*storage_size).move_to(sqr.get_center()).set_z_index(1)
            block = VGroup(sqr,num)
            block.move_to([3 + storage_distance*(i%8) , 2 - storage_distance*(i//8), 0])
            memorys.add(block)
        memorys_area = Rectangle(width = storage_buff*11 + storage_size*8, 
                                 height = 1 + storage_size*8 + storage_buff*5, 
                                 color=GREEN, fill_opacity=0.1).move_to([3 + storage_size*3.5 + storage_buff*3.5 , (storage_size+ storage_buff)*3, 0]).set_z_index(-11)
       
        memorys_value = [0]*memory_capacity
        memorys_text = Text('内存区域', font="Microsoft YaHei UI", font_size=32).move_to(memorys_area.get_top()).shift(DOWN*0.5).set_z_index(-10)
        self.add(memorys,memorys_area,memorys_text)
        

        #外存区域 建立乱序数组
        stores_length = len(stores_value)
        stores = VGroup()
        for i in range(stores_length):
            n = stores_value[i]
            sqr = square.copy().set_fill(color = num_to_color(n,'dark')).set_stroke(color = num_to_color(n,'light'))
            num = Text(str(n), font="Times New Roman", font_size=32*storage_size).move_to(sqr.get_center()).set_z_index(1)
            block = VGroup(sqr,num)
            block.move_to([-6.5 + storage_distance*(i%16) , 2 - storage_distance*(i//16), 0])
            stores.add(block)
        self.add(stores)


        #统计数据
        def updata_statistics(statistics, type = 'init', cost = 1):
            #statistics 是列表
            type_mapping = {'read': 0, 'write': 1, 'comparison': 2, 'assignment': 3, 'exchange': 4, 'point': 5, 'spoint': 6, 'mpoint': 7}
            typeindex = type_mapping.get(type, -1)
            #初始化 [0,'读出外存次数',  [1.5,-3.2,0], 说明文本, 数值文本]
            if type == 'init':
                statistics = [
                    [0,'读出外存次数',  [1.5,-3.2,0]],
                    [0,'写入外存次数',  [1.5,-3.6,0]],
                    [0,'比较元素次数',  [3.5,-2.8,0]],
                    [0,'赋值元素次数',  [3.5,-3.2,0]],
                    [0,'交换元素次数',  [3.5,-3.6,0]],
                    [0,'遍历元素次数',  [5.5,-2.8,0]],
                    [0,'遍历外存次数',  [5.5,-3.2,0]],
                    [0,'遍历内存次数',  [5.5,-3.6,0]]]
                for chain in statistics:
                    comment  = Text(chain[1], font="SimHei", font_size=32*storage_size).move_to(chain[2]).set_z_index(1)
                    value  = Text(str(chain[0]),  font="SimHei", font_size=32*storage_size).move_to(comment.get_right()  + RIGHT*0.4).set_z_index(1)
                    chain.append(comment)
                    chain.append(value)
                    self.add(comment,value)
                return statistics
            elif typeindex >= 0:
                statistics[typeindex][0] += cost
                if animation_generation:
                    self.play(statistics[typeindex][4].animate.become(Text(str(statistics[typeindex][0]), font="SimHei", font_size=32*storage_size).move_to(statistics[typeindex][4].get_center())), run_time = 0.1)
                return statistics
            elif type == 'sp_mp_point':
                statistics[5][0] += 2
                statistics[6][0] += 1
                statistics[7][0] += 1
                if animation_generation:
                    self.play(  statistics[5][4].animate.become(Text(str(statistics[5][0]), font="SimHei", font_size=32*storage_size).move_to(statistics[5][4].get_center())), 
                                statistics[6][4].animate.become(Text(str(statistics[6][0]), font="SimHei", font_size=32*storage_size).move_to(statistics[6][4].get_center())), 
                                statistics[7][4].animate.become(Text(str(statistics[7][0]), font="SimHei", font_size=32*storage_size).move_to(statistics[7][4].get_center())), run_time = 0.1)
            elif type == 'sp_point':
                statistics[5][0] += 1
                statistics[6][0] += 1
                if animation_generation:
                    self.play(  statistics[5][4].animate.become(Text(str(statistics[5][0]), font="SimHei", font_size=32*storage_size).move_to(statistics[5][4].get_center())), 
                                statistics[6][4].animate.become(Text(str(statistics[6][0]), font="SimHei", font_size=32*storage_size).move_to(statistics[6][4].get_center())), run_time = 0.1)
            elif type == 'mp_point':
                statistics[5][0] += 1
                statistics[7][0] += 1
                if animation_generation:
                    self.play(  statistics[5][4].animate.become(Text(str(statistics[5][0]), font="SimHei", font_size=32*storage_size).move_to(statistics[5][4].get_center())), 
                                statistics[7][4].animate.become(Text(str(statistics[7][0]), font="SimHei", font_size=32*storage_size).move_to(statistics[7][4].get_center())), run_time = 0.1)
            elif type == 'r_assignment':
                statistics[0][0] += 1
                statistics[3][0] += 1
                if animation_generation:
                    self.play(  statistics[0][4].animate.become(Text(str(statistics[0][0]), font="SimHei", font_size=32*storage_size).move_to(statistics[0][4].get_center())), 
                                statistics[3][4].animate.become(Text(str(statistics[3][0]), font="SimHei", font_size=32*storage_size).move_to(statistics[3][4].get_center())), run_time = 0.1)
            elif type == 'w_assignment':
                statistics[1][0] += 1
                statistics[3][0] += 1
                if animation_generation:
                    self.play(  statistics[1][4].animate.become(Text(str(statistics[1][0]), font="SimHei", font_size=32*storage_size).move_to(statistics[1][4].get_center())), 
                                statistics[3][4].animate.become(Text(str(statistics[3][0]), font="SimHei", font_size=32*storage_size).move_to(statistics[3][4].get_center())), run_time = 0.1)
            elif type == 'exchange_assignment':
                statistics[4][0] += 1
                statistics[3][0] += 1
                if animation_generation:
                    self.play(  statistics[4][4].animate.become(Text(str(statistics[4][0]), font="SimHei", font_size=32*storage_size).move_to(statistics[4][4].get_center())), 
                                statistics[3][4].animate.become(Text(str(statistics[3][0]), font="SimHei", font_size=32*storage_size).move_to(statistics[3][4].get_center())), run_time = 0.1)
            elif type == 'clear':
                for chain in statistics:
                    chain[0] = 0
                    if animation_generation:
                        self.play(chain[4].animate.become(Text(str(chain[0]), font="SimHei", font_size=32*storage_size).move_to(chain[4].get_center())), run_time = 0.1)
            else:     
                for chain in statistics:
                    self.remove(chain[3],chain[4])
                    chain[3]  = Text(chain[1], font="SimHei", font_size=32*storage_size).move_to(chain[2]).set_z_index(1)
                    chain[4]  = Text(str(chain[0]),  font="SimHei", font_size=32*storage_size).move_to(chain[3].get_right()  + RIGHT*0.4).set_z_index(1)
                    self.add(chain[3],chain[4])
                return statistics
        
        statistics = updata_statistics(statistics = [])


        #内存区域赋值 后者 赋值给 前者
        def memory_assignment(recipient_index, sender_index, exchange = 0):
            if animation_generation:
                replaceblock = memorys[sender_index].copy()
                replaceblock[0].set_z_index(2)
                replaceblock[1].set_z_index(3)
                self.play(replaceblock.animate.scale(0.5), run_time = 0.2, rate_func=smooth)
                self.play(replaceblock.animate.move_to(memorys[recipient_index]), run_time = 0.5, rate_func=smooth)
                self.play(replaceblock.animate.scale(2), run_time = 0.2, rate_func=smooth)
                self.remove(memorys[recipient_index])
                memorys[recipient_index]=replaceblock.copy()
                self.add(memorys[recipient_index])
                self.remove(replaceblock)
                memorys[recipient_index][0].set_z_index(0)
                memorys[recipient_index][1].set_z_index(1)
            else:
                self.remove(memorys[recipient_index])
                memorys[recipient_index] = memorys[sender_index].copy().move_to(memorys[recipient_index])
                self.add(memorys[recipient_index])    
            memorys_value[recipient_index]=memorys_value[sender_index]
            if exchange == 0:
                updata_statistics(statistics, 'assignment')
            else:
                updata_statistics(statistics, 'exchange_assignment')

        #读取外存区域 后者 赋值给 前者
        def read_stores(recipient_index, sender_index):
            if animation_generation == True:
                readblock = stores[sender_index].copy()
                readblock[0].set_z_index(2)
                readblock[1].set_z_index(3)
                self.play(readblock.animate.scale(0.5), run_time = 0.2, rate_func=linear)
                self.play(readblock.animate.shift(UP*storage_distance/2), run_time = 0.3, rate_func=linear)
                self.play(readblock.animate.move_to(memorys[recipient_index]).shift(UP*storage_distance/2), run_time = 0.9, rate_func=smooth)
                self.play(readblock.animate.shift(DOWN*storage_distance/2), run_time = 0.3, rate_func=linear)
                self.play(readblock.animate.scale(2), run_time = 0.2, rate_func=linear)
                self.remove(memorys[recipient_index])
                memorys[recipient_index] = readblock.copy()
                self.add(memorys[recipient_index])
                self.remove(readblock)
                memorys[recipient_index][0].set_z_index(0)
                memorys[recipient_index][1].set_z_index(1)
            else:
                self.remove(memorys[recipient_index])
                memorys[recipient_index] = stores[sender_index].copy().move_to(memorys[recipient_index])
                self.add(memorys[recipient_index])
            memorys_value[recipient_index] = stores_value[sender_index]
            updata_statistics(statistics, 'r_assignment')
        
        #写入外存区域 后者 赋值给 前者
        def write_stores(recipient_index, sender_index):
            if animation_generation == True:
                readblock = memorys[sender_index].copy()
                readblock[0].set_z_index(2)
                readblock[1].set_z_index(3)
                self.play(readblock.animate.scale(0.5), run_time = 0.2, rate_func=linear)
                self.play(readblock.animate.shift(UP*storage_distance/2), run_time = 0.3, rate_func=linear)
                self.play(readblock.animate.move_to(stores[recipient_index]).shift(UP*storage_distance/2), run_time = 0.9, rate_func=smooth)
                self.play(readblock.animate.shift(DOWN*storage_distance/2), run_time = 0.3, rate_func=linear)
                self.play(readblock.animate.scale(2), run_time = 0.2, rate_func=linear)
                self.remove(stores[recipient_index])
                stores[recipient_index] = readblock.copy()
                self.add(stores[recipient_index])
                self.remove(readblock)
                stores[recipient_index][0].set_z_index(0)
                stores[recipient_index][1].set_z_index(1)
            else:
                self.remove(stores[recipient_index])
                stores[recipient_index] = memorys[sender_index].copy().move_to(stores[recipient_index])
                self.add(stores[recipient_index])
            stores_value[recipient_index] = memorys_value[sender_index] 
            updata_statistics(statistics, 'w_assignment')

        #比较数据动画
        def memory_comparison(index_a,index_b):
            if animation_generation:
                self.play(memorys[index_a].animate.scale(1.1),memorys[index_b].animate.scale(1.1),run_time = 0.05, rate_func=linear)
                self.play(memorys[index_a].animate.scale(0.9/1.1),memorys[index_b].animate.scale(0.9/1.1),run_time = 0.05, rate_func=linear)
                self.play(memorys[index_a].animate.scale(1.1/0.9),memorys[index_b].animate.scale(1.1/0.9),run_time = 0.05, rate_func=linear)
                self.play(memorys[index_a].animate.scale(1.0/1.1),memorys[index_b].animate.scale(1.0/1.1),run_time = 0.05, rate_func=linear)
                if memorys_value[index_a] > memorys_value[index_b]:
                    self.play(memorys[index_a].animate.scale(1.2/1.0),memorys[index_b].animate.scale(0.8/1.0),run_time = 0.1, rate_func=linear)
                    self.wait(0.4)
                    self.play(memorys[index_a].animate.scale(1/1.2),memorys[index_b].animate.scale(1/0.8),run_time = 0.2, rate_func=linear)            
                elif memorys_value[index_a] < memorys_value[index_b]:
                    self.play(memorys[index_a].animate.scale(0.8/1.0),memorys[index_b].animate.scale(1.2/1.0),run_time = 0.1, rate_func=linear)
                    self.wait(0.4)
                    self.play(memorys[index_a].animate.scale(1/0.8),memorys[index_b].animate.scale(1/1.2),run_time = 0.2, rate_func=linear)
                elif memorys_value[index_a] == memorys_value[index_b]:
                    self.wait(0.7)
                updata_statistics(statistics, 'comparison')

        #新建指针
        def updata_pointer(pointer, area = 'memorys', index = None, pointer_color = None , pointer_name = 'Default'):
            #移动到 index 位置 或者 没有输入值时 移动到 pointer[1]
            if index == None:
                index = pointer[1]
            #传入的指针不是空列表 
            if pointer:
                print(f'移动{"内存" if area == "memorys" else ("外存" if area == "stores" else "")}指针 {pointer[0]} 到 {index} 位')
                if not pointer_color:
                    pointer_color = pointer[3]
                else:
                    pointer[3] = pointer_color
                if pointer_name == 'Default':
                    pointer_name = pointer[0]
                else:
                    pointer[0] = pointer_name
                pointer[1] = index
                if area == 'memorys':
                    if animation_generation:
                        self.play(pointer[2].animate.move_to(memorys[index].get_center()).set_color(pointer_color),run_time = 0.4, rate_func=smooth)
                    else:
                        self.remove(pointer[2])
                        self.add(pointer[2].move_to(memorys[index].get_center()).set_color(pointer_color))
                    updata_statistics(statistics, 'mp_point')
                elif area == 'stores':
                    if animation_generation:
                        self.play(pointer[2].animate.move_to(stores[index].get_center()).set_color(pointer_color),run_time = 0.4, rate_func=smooth)
                    else:
                        self.remove(pointer[2])
                        self.add(pointer[2].move_to(stores[index].get_center()).set_color(pointer_color))
                    updata_statistics(statistics, 'sp_point')
            else:
                print(f'新建{"内存" if area == "memorys" else ("外存" if area == "stores" else "")}指针 {pointer_name} 在 {index} 位')
                if not pointer_color:
                    pointer_color = RED
                if area == 'memorys':
                    new_mobpointer  = mobpointer.copy().set_color(color = pointer_color).move_to(memorys[index].get_top() + (pointer_size/2+ storage_buff)*UP ).rotate(PI).set_z_index(10)
                    new_boxpointer  = boxpointer.copy().set_color(color = pointer_color).move_to(memorys[index].get_center()).set_z_index(10)
                    updata_statistics(statistics, 'mp_point')
                elif area == 'stores':
                    new_mobpointer  = mobpointer.copy().set_color(color = pointer_color).move_to(stores[index].get_top() + (pointer_size/2+ storage_buff)*UP ).rotate(PI).set_z_index(10)
                    new_boxpointer  = boxpointer.copy().set_color(color = pointer_color).move_to(stores[index].get_center()).set_z_index(10)
                    updata_statistics(statistics, 'sp_point')
                if animation_generation:
                    self.play(Create(new_mobpointer),run_time = 0.2)
                    self.play(Transform(new_mobpointer,new_boxpointer), run_time = 0.2)
                else:
                    new_mobpointer = new_boxpointer.copy()
                    self.add(new_mobpointer)
                pointer = []
                pointer.append(pointer_name)
                pointer.append(index)
                pointer.append(new_mobpointer)
                pointer.append(pointer_color)
            return pointer
        
     


        #指针相关 先定义空指针
        pointer_ma, pointer_mb, pointer_mc, pointer_md, pointer_me, pointer_mf, pointer_mg, pointer_mh = [[] for _ in range(8)]
        pointer_sa, pointer_sb, pointer_sc, pointer_sd, pointer_se, pointer_sf, pointer_sg, pointer_sh = [[] for _ in range(8)]
        
        pointer_mw = []
        pointer_mr = []
        pointer_sw = []
        pointer_sr = []


        #归并相关指针
        minimerge_subset_pointer_lists = []
        minimerge_subset_pointer_count = 0

        merge_way_memory_pointer_lists = []
        merge_way_memory_terminus_lists = []
        merge_way_store_pointer_lists = []
        merge_way = 2

        #指针
        pointer_sa = updata_pointer(pointer_sa,'stores' ,0,GOLD,'Read')

        #修改最小归并子集
        subset_length = 8
        merge_time = 0
        #################
        #     START     #
        #################
        print(f'内存:[{memory_length}/{memory_capacity}]')
        while True:
            
            print('最小合并子集头指针位置指向读取位')
            minimerge_subset_pointer = updata_pointer([],'stores' ,pointer_sa[1], num_to_color(minimerge_subset_pointer_count*50),'Mini Merge Subset')
            minimerge_subset_pointer_lists.append(minimerge_subset_pointer)
            minimerge_subset_pointer_count += 1

            #################
            #  READ STORES  #
            #################
            #从指针指向位置 读取内存
            
            pointer_ma = updata_pointer(pointer_ma,'memorys',0,RED ,'A')
            
            for i in range(subset_length):
                if i != 0:
                    if pointer_ma[1]+1 >= memory_capacity:
                        print('Read: 超过内存范围 读外存结束')
                        return 0
                    
                    if pointer_sa[1]+1 >= stores_length:
                        print('Read: 超过外存范围 读外存结束')
                        break
                    pointer_ma[1] += 1
                    pointer_sa[1] += 1
                    #指针后移
                    pointer_ma = updata_pointer(pointer_ma,'memorys')
                    pointer_sa = updata_pointer(pointer_sa,'stores')

                #读取内存
                read_stores(pointer_ma[1],pointer_sa[1])
                memory_length += 1
                memory_spare -= 1
            print(f'内存:[{memory_length}/{memory_capacity}]')
            
            if memory_spare >= memory_length:
                print(f'剩余空间{memory_spare} [最小归并子集 ~ ')
                print('采用双列冒泡后归并排序')
                sort_type = 'bothsidebubbling_merge'
            elif 1 <= memory_spare < memory_length:
                print(f'剩余空间{memory_spare} [1 ~ 最小归并子集)')
                print('采用冒泡排序')
                sort_type = 'bubbling'
            else:
                print('没有空间排序了')
                break

            

            sort_type = 'bothsidebubbling_merge'
            sort_type = 'bubbling'
            
            sort_type = 'bothsidebubbling_merge'
            
            if sort_type == 'bothsidebubbling_merge':
                pointer_mb = updata_pointer(pointer_mb,'memorys',0,BLUE_D,'B')
                #冒泡排序
                bubbling_a = False
                bubbling_b = False
                bubbling_exchange_a = False
                bubbling_exchange_b = False
                bubbling_over_a = False
                bubbling_over_b = False
                bubbling_meet_a = False
                bubbling_meet_b = False
                while True:
                    #b头 c头 d尾 a尾
                    print(memorys_value)
                    print('=================================================')
                    for i in range(memory_length):
                        print(f'| {memorys_value[i]:>3} ',end='')
                    print(f'|')
                    mc = -2
                    md = -2
                    if pointer_mc:
                        mc = pointer_mc[1]
                    if pointer_md:
                        md = pointer_md[1]
                    for i in range(memory_length):
                        if i == pointer_mb[1]:
                            print('|  b  ',end='')
                        elif i == pointer_ma[1]:
                            print('|  a  ',end='')
                        elif i == mc:
                            print('|  c  ',end='')
                        elif i == md:
                            print('|  d  ',end='')
                        else:
                            print('|     ',end='')
                    print(f'|')
                    print('=================================================')
                    #最开始 A0 B0 M0 AE0 BE0 AO0 BO0
                    #第二循环 A0 B1 M0 AE0 BE0 AO0 BO0 一般不相遇->[A1 B0]
                    #第三循环 A1 B0 M0 AE0 BE0 AO0 BO0 假设相遇->[M1]
                    #第四循环 A0 B1 M0 AE0 BE0 AO0 BO0 一般不相遇->[A0 B1]
                    if -1 <= pointer_mb[1] - pointer_ma[1] <= 1:
                        print('AB指针相遇了')
                        bubbling_meet_a = True
                        bubbling_meet_b = True
                        pointer_me = updata_pointer(pointer_me,'memorys',pointer_ma[1],BLUE_E,'Merge2')
                    if pointer_mc:
                        if -1 <= pointer_mb[1] - pointer_mc[1] <= 1:
                            print('BC指针相遇了')
                            bubbling_meet_b = True
                    if pointer_md:
                        if -1 <= pointer_ma[1] - pointer_md[1] <= 1:
                            print('AD指针相遇了')
                            bubbling_meet_a = True
                    #长度过短时 A0 B0 [M1] AE0 BE0 AO0 BO0 
                    #最开始 A0 [B1] M0 AE0 BE0 AO0 BO0 
                    if bubbling_meet_a or bubbling_meet_b:
                        if bubbling_meet_b:
                            print('B完成了一趟冒泡')
                            if bubbling_exchange_b:
                                print('本轮B交换了元素')
                                bubbling_meet_b = False
                                bubbling_exchange_b = False
                                print('C指针移动到B位置')
                                pointer_mc = updata_pointer(pointer_mc,'memorys',pointer_mb[1],BLUE_A,'C')
                                print('B指针归位')
                                pointer_mb = updata_pointer(pointer_mb,'memorys',0)
                                if pointer_mc[1] == 1:
                                    print('B排指针冒泡结束')
                                    bubbling_over_b = True
                            else:
                                print('本轮B没交换元素 B指针固定')
                                bubbling_over_b = True
                        
                        if bubbling_meet_a:
                            if bubbling_exchange_a:
                                print('本轮A交换了元素')
                                bubbling_meet_a = False
                                bubbling_exchange_a = False
                                print('D指针移动到A位置')
                                pointer_md = updata_pointer(pointer_md,'memorys',pointer_ma[1],RED_A,'D')
                                print('A指针归位')
                                pointer_ma = updata_pointer(pointer_ma,'memorys',memory_length-1)
                                if pointer_md[1] == memory_length-2:
                                    print('A排指针冒泡结束')
                                    bubbling_over_a = True
                            else:
                                print('本轮A没交换元素 A指针固定')
                                bubbling_over_a = True
                        
                        if bubbling_over_a and bubbling_over_b == False:
                            print('A已经排序好 下回合继续走B')
                            bubbling_a = False
                            bubbling_b = True
                        elif bubbling_over_b and bubbling_over_a == False:
                            print('B已经排序好 下回合继续走A')
                            bubbling_a = True
                            bubbling_b = False
                        elif bubbling_over_b == False and bubbling_over_a == False:
                            print('A B 都暂未排序好 根据上回合情况走')
                    else:
                        print('指针未相遇 继续')
                    #长度过短时 A0 B0 M1 AE0 BE0 [AO1] [BO1] 跳出循环
                    #第三循环 A1 B0 M1 AE0 BE2 AO0 BO0 假设A没交换->[AO1]
                    if  bubbling_over_b and bubbling_over_a:
                        break
                    
                    #指针未相遇 继续
                    if bubbling_a == False and bubbling_b == False:
                        print('从B指针开始冒泡')
                        bubbling_b = True
                    elif bubbling_a == True and bubbling_b == False:
                        if bubbling_over_b == False:
                            print('上一个冒泡的是A指针 接下来B指针冒泡')
                            bubbling_b = True
                            bubbling_a = False
                    elif bubbling_a == False and bubbling_b == True:
                        if bubbling_over_a == False:
                            print('上一个冒泡的是B指针 接下来A指针冒泡')
                            bubbling_a = True
                            bubbling_b = False
                    else:
                        print('一般不会出现这种情况')
                    #最开始 A0 B1 M0 AE0 BE0 AO0 BO0 执行B
                    #第二循环 A1 B0 M0 AE0 BE0 AO0 BO0 跳过B
                    if bubbling_b:
                        #比较 首指针元素 和 首指针下一个元素
                        memory_comparison(pointer_mb[1],pointer_mb[1] + 1)
                        if memorys_value[pointer_mb[1]] > memorys_value[pointer_mb[1]+1]:
                            #赋值
                            memory_assignment(memory_capacity - 1,  pointer_mb[1])
                            memory_assignment(pointer_mb[1],      pointer_mb[1] + 1)
                            #指针后移
                            pointer_mb[1] += 1
                            pointer_mb = updata_pointer(pointer_mb,'memorys')
                            #赋值
                            memory_assignment(pointer_mb[1] ,  memory_capacity - 1, exchange = 1)
                            bubbling_exchange_b = True
                        else:   
                            #指针后移
                            pointer_mb[1] += 1
                            pointer_mb = updata_pointer(pointer_mb,'memorys')
                    #最开始 A0 B1 M0 AE0 BE0 AO0 BO0 跳过A
                    #第二循环 A1 B0 M0 AE0 BE0 AO0 BO0 执行A
                    if bubbling_a:
                        memory_comparison(pointer_ma[1], pointer_ma[1] - 1)
                        if memorys_value[pointer_ma[1] - 1] > memorys_value[pointer_ma[1]]:
                            #赋值
                            memory_assignment(memory_capacity - 1,  pointer_ma[1])
                            memory_assignment(pointer_ma[1],      pointer_ma[1] - 1)
                            #指针后移
                            pointer_ma[1] -= 1
                            pointer_ma = updata_pointer(pointer_ma,'memorys')
                            #赋值
                            memory_assignment(pointer_ma[1] ,  memory_capacity - 1, exchange = 1)
                            bubbling_exchange_a = True
                        else:
                            #指针后移
                            pointer_ma[1] -= 1
                            pointer_ma = updata_pointer(pointer_ma,'memorys')
                    #下一轮冒泡
                print('结束二路冒泡')

                
                

                pointer_ma = updata_pointer(pointer_ma,'memorys',0                  ,BLUE_B ,'A')
                pointer_mb = updata_pointer(pointer_mb,'memorys',pointer_me[1] - 1  ,BLUE_E ,'B')
                pointer_mc = updata_pointer(pointer_mc,'memorys',pointer_me[1]      ,RED_B  ,'C')
                pointer_md = updata_pointer(pointer_md,'memorys',memory_length - 1  ,RED_E  ,'D')
                pointer_me = updata_pointer(pointer_me,'memorys',memory_length      ,GREEN_B,'E')
                print('开始二路归并')
                
                merge_over_1 = False
                merge_over_2 = False
                while True:
                    if merge_over_1 == False and merge_over_2 == False:
                        memory_comparison(pointer_ma[1], pointer_mc[1])
                        minright = memorys_value[pointer_ma[1]] <= memorys_value[pointer_mc[1]]
                    else:
                        minright = True
                    '''
                    mini over1 over2
                    0     0     0   取2
                    0     0     1   取1
                    0     1     0   取2
                    0     1     1   不存在
                    1     0     0   取1
                    1     0     1   取1
                    1     1     0   取2
                    1     1     1   结束
                    '''
                    if (minright and not merge_over_1) or (not minright and not merge_over_1 and merge_over_2):
                        print('取1路元素')
                        #赋值
                        memory_assignment(pointer_me[1],  pointer_ma[1])
                        if pointer_ma[1] < pointer_mb[1]:
                            pointer_ma[1] += 1
                            pointer_ma = updata_pointer(pointer_ma)
                        else:
                            print('1路元素全取出')
                            merge_over_1 = True
                    elif (not minright and not merge_over_2) or (minright and merge_over_1 and not merge_over_2):
                        print('取2路元素')
                        #赋值
                        memory_assignment(pointer_me[1],  pointer_mc[1])
                        if pointer_mc[1] < pointer_md[1]:
                            pointer_mc[1] += 1
                            pointer_mc = updata_pointer(pointer_mc)
                        else:
                            print('2路元素取出')
                            merge_over_2 = True
                    if merge_over_1 and merge_over_2:
                        break
                    #指针后移
                    pointer_me[1] += 1
                    pointer_me = updata_pointer(pointer_me)
                print('结束二路归并')
                
                pointer_ma = updata_pointer(pointer_ma,'memorys',memory_length       ,BLUE_B ,'A')
                self.remove(pointer_mb[2])
                self.remove(pointer_mc[2])
                self.remove(pointer_md[2])
                self.remove(pointer_me[2])
                pointer_mb=[]
                pointer_mc=[]
                pointer_md=[]
                pointer_me=[]
            elif sort_type == 'bubbling':
                pointer_ma = updata_pointer(pointer_ma,'memorys',0)
                pointer_mb = updata_pointer(pointer_mb,'memorys',memory_length-1,BLUE,'B')
                bubbling_exchange = False
                
                while True:
                    
                    if pointer_ma[1] == pointer_mb[1]:                            
                        print('完成一趟冒泡')
                        if bubbling_exchange:
                            if pointer_mb[1] > 1:
                                print('有交换元素 下一趟')
                                pointer_mb = updata_pointer(pointer_mb,'memorys',pointer_ma[1]-1)
                                pointer_ma = updata_pointer(pointer_ma,'memorys',0)
                                bubbling_exchange = False
                            else:
                                break
                        else:
                            print('没有交换元素 冒泡结束')
                            break
                    print('比较 A指针元素 和 A指针下一个元素')
                    memory_comparison(pointer_ma[1],pointer_ma[1] + 1)
                    if memorys_value[pointer_ma[1]] > memorys_value[pointer_ma[1]+1]:
                        #赋值
                        memory_assignment(memory_capacity - 1,  pointer_ma[1])
                        memory_assignment(pointer_ma[1],      pointer_ma[1] + 1)
                        #指针后移
                        pointer_ma[1] += 1
                        pointer_ma = updata_pointer(pointer_ma,'memorys')
                        #赋值
                        memory_assignment(pointer_ma[1] ,  memory_capacity - 1, exchange = 1)
                        bubbling_exchange = True
                    else:   
                        #指针后移
                        pointer_ma[1] += 1
                        pointer_ma = updata_pointer(pointer_ma,'memorys')
                
                
                self.remove(pointer_mb[2])
                pointer_mb=[]
                pointer_ma = updata_pointer(pointer_ma,'memorys',0)
            else:
                print('没选择排序算法')
            print('写入外存')
            print(f'目前Mini Merge Subset数量:{minimerge_subset_pointer_count}')
            print(f'位置是:{minimerge_subset_pointer_lists[minimerge_subset_pointer_count-1][1]}')
            pointer_sa = updata_pointer(pointer_sa,'stores',minimerge_subset_pointer_lists[minimerge_subset_pointer_count-1][1])
            for i in range(memory_length,memory_length*2):
                if i > memory_length:
                    pointer_ma[1] += 1
                    pointer_sa[1] += 1
                    pointer_ma = updata_pointer(pointer_ma,'memorys')
                    pointer_sa = updata_pointer(pointer_sa,'stores')
                write_stores(pointer_sa[1], pointer_ma[1])
                memory_length -= 1
                memory_spare  += 1
            print('写完外存')    
            if pointer_sa[1] < stores_length - 1:
                print('外存还有元素没排序')
                pointer_sa[1] += 1
                pointer_sa = updata_pointer(pointer_sa,'stores')
            else:
                print('排序完了')
                self.remove(pointer_ma[2])
                self.remove(pointer_sa[2])
                pointer_ma=[]
                pointer_sa=[]
                break
            merge_time += 1
        print('可以开始外部归并')
        pointer_sw = updata_pointer(pointer_sw,'stores',0,GRAY_D,'Write')
        pointer_sr = updata_pointer(pointer_sr,'stores',0,GRAY_B,'Read')
        for i in minimerge_subset_pointer_lists:
            print(i)
        minimerge_subset_pointer_index = 0
        print(f'开始一轮外部归并')
        while True:
            pointer_mw = updata_pointer(pointer_mw,'memorys',0,GRAY_D,'Write')
            pointer_mr = updata_pointer(pointer_mr,'memorys',0,GRAY_B,'Read')

            print(f'把条 {merge_way}')
              #  animation_generation = True
            for i in range(merge_way):
                # k == 1: animation_generation = True
                if i > 0:
                    pointer_sr[1] += 1
                    pointer_mw[1] += 1
                    pointer_mw = updata_pointer(pointer_mw,'memorys')
                print(f'从外存{pointer_sr[1]}开始读取{i+1}/{merge_way}个子集合成归并集 目前是{minimerge_subset_pointer_index}号子集')
                pointer_sr = updata_pointer(pointer_sr,'stores',pointer_sr[1])
                if i == 0:
                    print(f'记录本次归并集的外存位置 {pointer_sr[1]} ')
                    merge_way_store_pointer = updata_pointer([],'stores', pointer_sr[1] ,num_to_color(i*100,'grey'),'Merge Store Way')
                    merge_way_store_pointer_lists.append(merge_way_store_pointer)

                print(f'记录 处于{pointer_mw[1]} 的 {i+1}/{merge_way}号子集')
                merge_way_memory_pointer = updata_pointer([],'memorys', pointer_mw[1] ,num_to_color(i*100,'grey'),'Merge Memory Way')
                merge_way_memory_pointer_lists.append(merge_way_memory_pointer)

                print(f'目前归并集{len(merge_way_store_pointer_lists)} 子集 {len(merge_way_memory_pointer_lists)}')
                while True:
                    read_stores(pointer_mw[1],pointer_sr[1])
                    if minimerge_subset_pointer_index + 1 < len(minimerge_subset_pointer_lists):
                        print('当前读取的子集 后面还有子集')
                        if pointer_sr[1] + 1 == minimerge_subset_pointer_lists[minimerge_subset_pointer_index + 1][1]:
                            break
                    else:
                        print('当前读取的子集 后面没有子集')
                        if pointer_sr[1] + 1 >= len(stores_value):
                            break
                    pointer_sr[1] += 1
                    pointer_mw[1] += 1
                    pointer_sr = updata_pointer(pointer_sr,'stores')
                    pointer_mw = updata_pointer(pointer_mw,'memorys')

                print(f'记录 处于{pointer_mw[1]} 的 {i+1}/{merge_way}号子集尾')
                merge_way_memory_pointer = updata_pointer([],'memorys', pointer_mw[1] ,num_to_color(i*100,'grey'),'Merge Memory End')
                merge_way_memory_terminus_lists.append(merge_way_memory_pointer)
                minimerge_subset_pointer_index += 1
            
            print(f'开始一次外部归并 路数 {merge_way}')
            
            while True:
                pointer_mr = updata_pointer(pointer_mr,'memorys',merge_way_memory_pointer_lists[0][1],None,'Mini')
                minisubset = 0
                for mwmpointer in merge_way_memory_pointer_lists:
                    if mwmpointer[1] != pointer_mr[1]:
                        memory_comparison(pointer_mr[1],mwmpointer[1])
                        if memorys_value[pointer_mr[1]] > memorys_value[mwmpointer[1]]:
                            pointer_mr = updata_pointer(pointer_mr,'memorys',mwmpointer[1])
                            minisubset = merge_way_memory_pointer_lists.index(mwmpointer)
                
                print(f'找到最小元素 是{minisubset}号子集')
                write_stores(pointer_sw[1],pointer_mr[1])
                
                if merge_way_memory_pointer_lists[minisubset][1] < merge_way_memory_terminus_lists[minisubset][1]:
                    merge_way_memory_pointer_lists[minisubset][1] += 1
                    merge_way_memory_pointer_lists[minisubset] = updata_pointer(merge_way_memory_pointer_lists[minisubset],'memorys')
                else:
                    self.remove(merge_way_memory_pointer_lists[minisubset][2])
                    self.remove(merge_way_memory_terminus_lists[minisubset][2])
                    del merge_way_memory_pointer_lists[minisubset]
                    del merge_way_memory_terminus_lists[minisubset]
                if not merge_way_memory_pointer_lists:
                    print('合并结束')
                    break
                else:
                    pointer_sw[1] += 1
                    pointer_sw = updata_pointer(pointer_sw,'stores')
            
            if pointer_sw[1] + 1 < len(stores_value):
                pointer_sw[1] += 1
                pointer_sw = updata_pointer(pointer_sw,'stores')
                pointer_sr[1] += 1
                pointer_sr = updata_pointer(pointer_sr,'stores')
            else:
                break
                
            if minimerge_subset_pointer_index == 4: return 0
            '''
            if merge_way_store_pointer_lists[pointer_ma[1]][1] + 1 == 16:
                print('归并段取空')
                break
            else:
                merge_way_store_pointer_lists[pointer_ma[1]][1] += 1
                merge_way_store_pointer_lists[pointer_ma[1]] = updata_pointer(merge_way_store_pointer_lists[pointer_ma[1]],'stores')
                read_stores(pointer_ma[1],merge_way_store_pointer_lists[pointer_ma[1]][1])
            
            
            if k ==11:
                animation_generation = True
            if k ==15:
                print(merge_way_store_pointer_lists)
                return 0
            k += 1
            '''
        return None

            