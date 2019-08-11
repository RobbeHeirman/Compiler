from Nodes.ConditionalNodes.IfNode import IfNode


class WhileNode(IfNode):

    def generate_llvm(self, c_comment: bool = True):
        nw_label =
