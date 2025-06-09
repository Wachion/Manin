from manim import *

class BuildFullBinaryTree(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)
        deep = 7  # 定义树的深度
        cshift = 0.1
        vshift = 0.5
        node_radius = 0.05
        shift_time = 0.5
        node_root = Circle(radius=node_radius, color=BLACK, fill_opacity=1)  # 创建根节点
        self.play(Create(node_root),run_time = 0.5)  # 创建根节点的动画
        # 定义二叉树列表 
        # 使用 CL = ROOT*2+1 CR = ROOT*2+2 访问左右节点 [3]*2+1 => [7]
        # ROOT = (C-1)//2    [3]-1//2 = [1] [4]-1//2 = [1]
        # 使用 range( 2**(h-1)-1 , 2**h-1 ) 获取第h层地址 [2**(h-1)-1 ,  2**h-2] 
        # 每层节点数 2**(h-1)  左半部分地址 [2**(h-1) - 1 ,  3*2**(h-2) - 2] 右半部分地址 [3*2**(h-2) - 1 , 2**h - 2]
        binary_tree = [node_root]
        # 创建关于根的线
        root_line = Line(node_root.get_center(), node_root.get_center(), color=WHITE).set_z_index(-1)
        binary_tree_lines = [root_line]
        # 创建下一深度的节点
        for i in range(deep - 1):
            # 开始创建第 i+2 层
            # 所有节点向上移动
            up_node = VGroup(binary_tree,binary_tree_lines)
            self.play(up_node.animate.shift(UP*vshift))
            # 节点散开 创建第2层 i=0 时不会进入
            spread_movement = []
            for h in range(2,i+2):
                #[i=1]2层树[h=2] 此时在创建第3层过程中
                #[i=2]3层树[h=2,3] 此时在创建第4层过程中
                salhns = int(2**(h-1) - 1)
                ealhns = int(3*2**(h-2) - 2)
                sarhns = int(3*2**(h-2) - 1)
                earhns = int(2**h - 2)
                #Starting/Ending address of the left/right half nodes
                #[h=2]地址为 lhns = 1 rhns = 2
                #[h=3]地址为 lhns = 3 4 rhns = 5 6
                #越靠外的节点偏移量越大
                #创建第3层时[i=1][h=2] [1]->1
                
                #创建第4层时[i=2][h=2] [1]->2
                #创建第4层时[i=2][h=3] [3]->3 [4]->1

                #创建第5层时[i=3][h=2] (i-h+1)=2 [1]->4
                #创建第5层时[i=3][h=3] (i-h+1)=1 [3]->6 [4]->2
                #创建第5层时[i=3][h=4] (i-h+1)=0 [7]->9 [8]->5 [9]->3 [10]->1
                for lnode in range(salhns ,  ealhns+1):
                    offset = ((ealhns - lnode)*2 + 1)*(2**(i-h+1))*cshift
                    spread_movement.append(binary_tree[lnode].animate.shift(LEFT*offset))
                    # 左右子节点对父节点的连线
                    pnode = (lnode-1)//2
                    #[i=1][h=2]2层树 移动第2层 lhns =  1  1 rhns =  2  2 pnode = 0   poffset = 0

                    #[i=2][h=2]3层树 移动第2层 lhns =  1  1 rhns =  2  2 pnode = 0
                    #[i=2][h=3]3层树 移动第3层 lhns =  3  4 rhns =  5  6 pnode = 1   poffset = 1 * 2^1 = 2

                    #[i=3][h=2]4层树 移动第2层 lhns =  1  1 rhns =  2  2 pnode = 0
                    #[i=3][h=3]4层树 移动第3层 lhns =  3  4 rhns =  5  6 pnode = 1   poffset = 1 * 2^2 = 4
                    #[i=3][h=4]4层树 移动第3层 lhns =  7 10 rhns = 11 14 pnode = 3 4 poffset = 3 * 2^1 = 6
                    if pnode == 0:
                        poffset = 0
                    else:
                        poffset = (((ealhns-1)//2 - pnode)*2 + 1)*(2**(i-h+2))*cshift
                    spread_movement.append(
                        binary_tree_lines[lnode].animate.put_start_and_end_on(
                            binary_tree[pnode].get_center()+LEFT*poffset, binary_tree[lnode].get_center()+LEFT*offset))
                    
                for rnode in range(sarhns ,  earhns+1):
                    offset = ((rnode - sarhns)*2 + 1)*(2**(i-h+1))*cshift
                    spread_movement.append(binary_tree[rnode].animate.shift(RIGHT*offset))
                    # 左右子节点对父节点的连线
                    pnode = (rnode-1)//2
                    if pnode == 0:
                        poffset = 0
                    else:
                        poffset = ((pnode - (sarhns-1)//2)*2 + 1)*(2**(i-h+2))*cshift
                    spread_movement.append(
                        binary_tree_lines[rnode].animate.put_start_and_end_on(
                            binary_tree[pnode].get_center()+RIGHT*poffset, binary_tree[rnode].get_center()+RIGHT*offset))    
            #播放散开过程
            if spread_movement:
                self.play(spread_movement,run_time = shift_time)
            # 遍历最末层的所有节点 [i=0] 遍历第1层 sa,ea 0 0
            sa = int(2**(i) - 1)
            ea = int(2**(i+1) - 2)
            create_nodes = []
            create_lines = []
            for bi in range(sa,ea+1):
                # 创建左右子节点
                node_l = Circle(radius=node_radius, color=BLUE, fill_opacity=1).shift(LEFT*cshift)
                node_r = Circle(radius=node_radius, color=RED, fill_opacity=1).shift(RIGHT*cshift)
                # 将左右子节点移动到当前节点下方
                node = VGroup(node_l,node_r)
                node.move_to(binary_tree[bi].get_center()).shift(DOWN*vshift)
                # 将左右子节点加入列表
                binary_tree.append(node_l)
                binary_tree.append(node_r)
                create_nodes.append(Create(node_l))
                create_nodes.append(Create(node_r))
                
                # 创建关于左右子节点的连线,buff=node_radius,buff=node_radius
                lnode_line = Line(binary_tree[bi].get_center(), node_l.get_center(), color=WHITE).set_z_index(-1)
                rnode_line = Line(binary_tree[bi].get_center(), node_r.get_center(), color=WHITE).set_z_index(-1)
                binary_tree_lines.append(lnode_line)
                binary_tree_lines.append(rnode_line)
                create_lines.append(Create(lnode_line))
                create_lines.append(Create(rnode_line))

            # 播放创建底部节点的动画
            
            if create_lines and create_nodes:
                self.play(create_lines,create_nodes)
        self.wait(2)