#!/usr/bin/python2.4
"""
drawtree.py

Author: Rick Ree (rree at post dot harvard dot edu)
Requirements:
 * Python 2.x (http://www.python.org)
 * reportlab (http://www.reportlab.com)
 * Mavric (http://bioinformatics.org/mavric)

Last revision: Thu Mar 13 22:06:18 PST 2003
"""
import sys, os, re, math
import reportlab.pdfgen.canvas
import reportlab.lib.pagesizes
import reportlab.graphics.widgetbase
from reportlab.graphics import shapes
from reportlab.pdfbase import pdfmetrics
from reportlab.graphics import renderPS
from reportlab.lib import colors
import newick, phylo, tree_compare

import optparse

PG_SIZE = reportlab.lib.pagesizes.letter

USAGE = """
Render a newick-formatted tree as a PDF or EPS file.

  %prog [options] infile
"""

def parse_options():
    parser = optparse.OptionParser(usage=USAGE)

    parser.add_option(
        "-o", "--outfile",
        action="store", type="string", dest="outfile", default=None,
        help="destination file for rendered tree "
        "(defaults to INFILE.pdf)"
        )
    parser.add_option(
        "--format",
        action="store", type="string", dest="format", default="pdf",
        help="output format (may also be specified by extension of output filename); "
        "choices are pdf (default) or eps"
        )
    parser.add_option(
        "-c", "--cladogram",
        action="store_false", dest="draw_phylogram",
        help="draw tree as a cladogram (default)"
        )
    parser.add_option(
        "-p", "--phylogram",
        action="store_true", dest="draw_phylogram",
        help="draw tree as a phylogram"
        )
    parser.add_option(
        "-t", "--title",
        action="store", type="string", dest="title", default=None,
        help="title of the tree"
        )
    parser.add_option(
        "-f", "--fill",
        action="store_true", dest="fill_page",
        help="scale drawing to fill page (default not filled)"
        )
    parser.add_option(
        "-v", "--verbose",
        action="store_true", dest="verbose",
        help="verbose mode"
        )
    parser.add_option(
        "-s", "--scale",
        action="store", type="float", dest="scale", default=None,
        help="scale branches by SCALE (default is automatic)"
        )
    parser.add_option(
        "--visible",
        action="store", type="string", dest="visible", default=[],
        help="comma-separated list of node attributes to show; "
        "possible values include 'support' and 'length'"
        )
    parser.add_option(
        "--support",
        action="store_true", dest="lengths_are_support",
        help="interpret branch lengths as support values "
        "(suppresses labeling tip branches)"
        )
    parser.add_option(
        "--thicken",
        action="store", type="float", dest="thicken", default=None,
        help="thicken branches that are strongly supported (>=THICKEN)"
        )
    parser.add_option(
        "--dsdn",
        action="store_true", dest="dsdn",
        help="experimental; "
        "first line of file should have S and N values, "
        "followed by 2 trees: "
        "first tree has dS values as lengths, second has dN"
        )

    return parser.parse_args()
       

def main():
    opts, args = parse_options()

    if args:
        infile = args[0]
    else:
        print >> sys.stderr, "No input file specified."
        sys.exit(1)

    ext = opts.format

    if infile == "-":
        infile = sys.stdin
        opts.outfile = opts.outfile or "stdout.%s" % ext
    else:
        opts.outfile = opts.outfile or "%s.%s" % (infile, ext)
        infile = open(infile)

    tree = get_input_tree(infile, opts)

##     if opts.outgroup:
##         print opts.outgroup
##         reroot(tree, [opts.outgroup])

    if opts.visible:
        opts.visible = opts.visible.split(",")

    render(tree, opts, center=1)

class Treestyle:
    cladogram = 0
    phylogram = 1

class DrawingNode(reportlab.graphics.widgetbase.Widget):
    """
    A node on a phylogeny that knows how to render itself, by drawing a
    line to its parent (if it has one) and drawing any associated
    labels: thus far, taxon, length, and support.  The position, size,
    font, etc. of these labels are specified in the node's XXX_render
    dictionaries (these are stored in the node's render_info
    dictionary).  If the 'visible' flag is set to 0, the label is not
    drawn.
    """
    base_render = {"visible": 1,
                   "x_offset": 0.5,
                   "y_offset": -0.33,
                   "offset_relative": "self",
                   "format": "%s",
                   "font": "Times-Roman",
                   "font_size": 1.0,
                   "font_color": colors.black,
                   "text_anchor": "start"}
    
    def __init__(self):
        self.children = []
        self.parent = None
        self.taxon = None
        self.length = None
        self.depth = 0  # number of internodes from root

        self.drawables = []

        self.x = 0.0
        self.y = 0.0

        # baseheight: the 'base' point size of the rendered node,
        # against which other attributes are rendered (labels etc.)
        self.baseheight = 12.0

        length_render = self.base_render.copy()
        length_render.update(
            {"visible": 0,
             "x_offset": 0,
             "y_offset": 0.25,
             "offset_relative": "edge",
             "format": "%g",
             "font": "Helvetica",
             "font_size": 0.75,
             "text_anchor": "middle"}
            )

        support_render = self.base_render.copy()
        support_render.update(
            {"visible": 0,
             "x_offset": 0,
             "y_offset": 0.25,
             "offset_relative": "edge",
             "format": "%0.2f",
             "font": "Helvetica",
             "font_size": 0.75,
             "text_anchor": "middle"}
            )
        dsdn_render = self.base_render.copy()
        dsdn_render.update(
            {"visible": 0,
             "x_offset": 0,
             "y_offset": 0.2,
             "offset_relative": "edge",
             "format": "%s",
             "font": "Helvetica",
             "font_size": 0.75,
             "text_anchor": "middle"}
            )

        self.render_info = {
            "taxon": self.base_render.copy(),
            "length": length_render,
            "support": support_render,
            "dsdn": dsdn_render
            }

        # vpad: proportion of label font size that separates ('pads')
        # terminal nodes
        # TODO: allow for multiline labels?
        self.vpad = 1.5

        # stroke_width: line thickness of drawn branches, as a
        # proportion of baseheight
        self.stroke_width = 0.1
        self.stroke_color = colors.black

    def set_attr(self, key, value, recurse=1):
        setattr(self, key, value)
        if recurse:
            for c in self.children:
                c.set_attr(key, value, recurse)

    def foreach(self, func):
        "call func with self as arg and recurse"
        func(self)
        for c in self.children:
            c.foreach(func)

    def set_render_attr(self, key, attr, value, recurse=1):
        self.render_info[key][attr] = value
        if recurse:
            for c in self.children:
                c.set_render_attr(key, attr, value, recurse)

    def calc_taxon_font_size(self):
        return self.baseheight * \
               self.render_info["taxon"]["font_size"]
    
    def calc_vpad(self):
        return max(self.baseheight * self.vpad,
                   self.calc_taxon_font_size() * self.vpad)

    def calc_strokewidth(self):
        return self.baseheight * self.stroke_width

    def calc_length_to_root(self):
        v = 0.0; n = self
        while n.parent is not None:
            v += n.length
            n = n.parent
        return v

    def translate(self, dx=0.0, dy=0.0, func=None):
        if func is not None:
            dx, dy = func(self)
        self.x += dx
        self.y += dy

        for d in self.drawables:
            d.translate(dx, dy)

        for c in self.children:
            c.translate(dx, dy, func)

    def add_child(self, child):
        self.children.append(child)
        child.x = self.x

    def get_height(self):
        if self.children:
            return reduce(lambda x,y: x+y,
                          [c.get_height() for c in self.children])
        else:
            return self.calc_vpad()

    def leaves(self, lvs = []):
        if self.children:
            for c in self.children:
                c.leaves(lvs)
        else:
            lvs.append(self)
        return lvs

    def sort(self):
        if self.children:
            data = [c.sort() for c in self.children]
            data.sort()
            if not filter(lambda x:x[0] != data[0][0], data):
                data.reverse()
            self.children[:] = [d[2] for d in data]
            return [reduce(lambda x,y:x+y, [d[0] for d in data]),
                    reduce(lambda x,y:x+y, [d[1] for d in data]),
                    self]
        else:
            return [1, [self.taxon], self]

    def draw(self):
        """render the node as a Group, recursively adding rendered
        child nodes"""
        
        g = shapes.Group()

        for attr, info in filter(lambda x:x[1]["visible"],
                                 self.render_info.items()):
            if hasattr(self, attr):
                val = getattr(self, attr)
                if val is not None:
                    fs = info["font_size"] * self.baseheight
                    rel = info["offset_relative"]
                    y = self.y
                    if rel == "self":
                        x = self.x
                    elif rel == "edge" and self.parent:
                        x = self.x - (self.x-self.parent.x)*0.5
                    dx = info["x_offset"] * fs
                    dy = info["y_offset"] * fs
                    label = shapes.String(
                        x + dx, y + dy,
                        info["format"] % val,
                        fontName = info["font"],
                        fontSize = fs,
                        fillColor = info["font_color"],
                        textAnchor = info["text_anchor"]
                    )
                    g.add(label)

        if self.parent:
            pl = shapes.PolyLine(
                [self.x, self.y,
                 self.parent.x, self.y,
                 self.parent.x, self.parent.y],
                strokeWidth = max(self.calc_strokewidth(), 1.0),
                strokeColor = self.stroke_color
                )
            g.add(pl)

            ## thicken strongly supported branches
            try:
                if self.thicken:
                    pl = shapes.PolyLine(
                        [self.x, self.y,
                         self.parent.x - self.parent.calc_strokewidth()/2.0, self.y],
                        strokeWidth = max(self.calc_strokewidth(), 1.0)*4,
                        strokeColor = self.stroke_color
                        )
                    g.add(pl)
            except AttributeError:
                pass

        for d in self.drawables:
            g.add(d)

        for c in self.children:
            g.add(c.draw())
            
        return g

def traverse(node, parent_gnode = None, mapping={}):
    """take a tree of phylo.Fnode's and return a tree of widget DrawingNodes"""
    if parent_gnode is None:
        parent_gnode = DrawingNode()
        parent_gnode.x = parent_gnode.y = 0.0
        parent_gnode.depth = 0
    else:
        n = DrawingNode()
        mapping[node] = n
        n.depth = parent_gnode.depth + 1
        n.parent = parent_gnode
        if node.label:
            n.taxon = node.label
        else:
            n.render_info["taxon"]["visible"] = 0
        n.length = node.length

##         if n.length is not None and n.parent and n.parent.length is not None:
##             n.length_to_root = n.length + n.parent.length_to_root

        parent_gnode.add_child(n)
        parent_gnode = n

    if node and not node.istip:
        for child in node.children():
            traverse(child, parent_gnode, mapping)

    return parent_gnode, mapping

def set_terminal_ypos(node, v = [None]):
    if node.children:
        children = node.children[:]
        for c in children:
            set_terminal_ypos(c, v)
    else:
        if v[0]:
            node.y = v[0].y + node.get_height()
        else:
            node.y = 0.0
        v[0] = node

def calc_internal_ypos(node):
    if node.children:
        map(calc_internal_ypos, node.children)
        
        node.y = (node.children[-1].y + node.children[0].y)*0.5

def calc_xpos(node, maxdepth, unitwidth):
    if node.parent:
        node.x = node.parent.x + unitwidth
    if node.children:
        for c in node.children:
            calc_xpos(c, maxdepth, unitwidth)
        if node.parent:
            node.x = node.parent.x + \
                     (min([n.x for n in node.children]) - node.parent.x)/2.0
    else:
        node.x += (maxdepth-node.depth)*unitwidth

def smooth_xpos(node):
    for c in node.children:
        smooth_xpos(c)
        
    if node.parent and node.children:
        px = node.parent.x
        cx = min([c.x for c in node.children])
        dxp = node.x - px
        cxp = cx - node.x
        node.x = px + (cx - px)*0.5
        

def scale_branches(node, scalefactor):
    if node.parent:
        node.x = node.parent.x + (node.length * scalefactor)
    for c in node.children:
        scale_branches(c, scalefactor)


def render(tree, opts, center=1, fill=0):
    pagesizes = reportlab.lib.pagesizes

    if opts.pagesize:
        size = {
            "letter": pagesizes.LETTER,
            "legal": pagesizes.LEGAL,
            "11x17": pagesizes.ELEVENSEVENTEEN,
            "A4": pagesizes.A4,
            }.get(opts.pagesize) or PG_SIZE
    else:
        size = PG_SIZE

    position=(0,0)

    border = min(size) * 0.05
    avail_w = size[0] - 2*border; avail_h = size[1] - 2*border

    for attr in opts.visible:
        tree.set_render_attr(attr, "visible", 1, 1)

    leaves = tree.leaves()

    maxdepth = max([leaf.depth for leaf in leaves])

    set_terminal_ypos(tree)
    calc_internal_ypos(tree)

    maxleaf = leaves[-1]
    maxy = maxleaf.y

    minleaf = leaves[0]
    miny = minleaf.y

    height = maxy - miny
    height *= 1.2

    # if fill: height = avail_h

    max_labelwidth = max(
        [pdfmetrics.stringWidth(
            str(l.taxon),
            l.render_info["taxon"]["font"],
            l.calc_taxon_font_size()
            ) + l.render_info["taxon"]["x_offset"] * l.baseheight
         for l in leaves]
        )

    unitwidth = (height*(avail_w/avail_h)) / maxdepth

    calc_xpos(tree, maxdepth, unitwidth)
    for i in range(10):
        smooth_xpos(tree)

    tree.translate(tree.calc_strokewidth()/2.0,
                   tree.calc_taxon_font_size()/2.0)

    width = (maxdepth * unitwidth) + \
            max_labelwidth + (tree.calc_strokewidth() * 0.5)
    width *= 1.2

    # if fill: width = avail_w

    if opts.lengths_are_support:
        def func(n):
            if n.length is not None:
                n.support = n.length
                n.length = None
                if not n.children:
                    n.support = None
        tree.foreach(func)

    if opts.thicken is not None:
        def func(n):
            try:
                if n.support >= opts.thicken:
                    n.thicken = 1
            except AttributeError:
                pass
        tree.foreach(func)

    if opts.draw_phylogram:
        if opts.scale:
            brlen_transform = opts.scale
        else:
            brlen_transform = (maxdepth * unitwidth) * \
                              1.0/max([l.calc_length_to_root() for l in leaves])
        scale_branches(tree, brlen_transform)
        if opts.verbose:
            print "%s: brlen_transform=%s" % (opts.outfile, brlen_transform)

        # draw scalebar
        leaves = tree.leaves()
        max_length_to_root = max([n.calc_length_to_root() for n in leaves])
        max_x = max([n.x for n in leaves])
        scalebar = shapes.Group()
        font_size = tree.calc_taxon_font_size()*0.9
        scalebar.add(shapes.String(max_x, tree.baseheight-font_size*(1.0/3.0),
                                   " %s" % str(max_length_to_root),
                                   textAnchor="start", fontSize=font_size))
        scalebar.add(shapes.String(tree.x, 1, "0.0",
                                   textAnchor="middle", fontSize=font_size))
        scalebar.add(shapes.Line(tree.x, tree.baseheight, max_x, tree.baseheight,
                                 strokeColor = colors.black, strokeWidth = 1.0))
        scalebar.add(shapes.Line(tree.x, tree.baseheight*1.2, tree.x, tree.baseheight*0.8,
                                 strokeColor = colors.black, strokeWidth = 1.0))
        scalebar.add(shapes.Line(max_x, tree.baseheight*1.2, max_x, tree.baseheight*0.8,
                                 strokeColor = colors.black, strokeWidth = 1.0))

        interval = 10**(math.floor(math.log10(float(max_length_to_root))))
        nintervals = int(math.modf(max_length_to_root/interval)[1])
        if nintervals == 1:
            interval = interval/4.0
        x = interval
        while x < max_length_to_root:
            scalebar.add(shapes.Line(x * brlen_transform, tree.baseheight*1.2,
                                     x * brlen_transform, tree.baseheight*0.8,
                                     strokeColor = colors.black, strokeWidth = 0.5))
            scalebar.add(shapes.String(x * brlen_transform, 1, str(x),
                                       textAnchor="middle", fontSize=font_size))
            x += interval
            
        
        height += tree.baseheight*3
        tree.translate(0, tree.baseheight*3)
        tree.drawables.append(scalebar)
                      
    if opts.title:
        font_size = tree.calc_taxon_font_size()
        title = shapes.Group()
        title.add(shapes.String(width*0.5, tree.x + height + font_size*3, opts.title,
                                textAnchor="middle", fontSize=font_size))
        tree.drawables.append(title)
        height += font_size*3
                  
    dwidth = width*1.2; dheight = height*1.2
    if fill:
        dwidth = avail_w; dheight = avail_h
    drawing = shapes.Drawing(dwidth, dheight)
    drawing.add(tree)

    scalefact = min(avail_w/float(width), avail_h/float(height))
    if not fill:
        scalefact = min(1.0, scalefact)

    ext = opts.outfile[-3:]
    if ext == "eps":
        opts.format = "eps"
        
    if opts.format == "pdf" and center:
        if height*scalefact < avail_h:
            tree.translate(0.0, (avail_h-height*scalefact) * 0.5/scalefact)
        if width*scalefact < avail_w:
            tree.translate((avail_w-width*scalefact) * 0.5/scalefact, 0.0)

    drawing.scale(scalefact, scalefact)
##     drawing.width = drawing.width * scalefact
##     drawing.height = drawing.height * scalefact

    if opts.format == "pdf":
        canvas = reportlab.pdfgen.canvas.Canvas(opts.outfile, size)
        canvas.setFont("Times-Roman", 10)

        drawing.drawOn(canvas, position[0]+border, position[1]+border)
        canvas.showPage()
        canvas.save()

    elif opts.format == "eps":
        if center:
            tree.translate(width*0.1, height*0.1)
        renderPS.drawToFile(drawing, opts.outfile)

    else:
        print >> sys.sterr, "Unknown file type, %s" % opts.format
        sys.exit(1)

def reroot(node, labels):
    p = phylo.most_recent_common_ancestor(node, labels).next
    q = p.next
    while q.next != p: q = q.next

    node.prune()

    node.data = p.data
    node.next = p; q.next = node

    for n in node.descendants():
        if n.back:
            if n.length is not None and n.back.length is None:
                n.back.length = n.length
            elif n.back.length is not None and n.length is None:
                n.length = n.back.length
    return node

TRANSPAT = re.compile(r'\btranslate\s+([^;]+);',
                      re.IGNORECASE | re.MULTILINE)
TREEPAT = re.compile(r'\btree\s+([_.\w]+)\s+=[^(]+(\([^;]+;)',
                     re.IGNORECASE | re.MULTILINE)
def get_trees_from_nexus(infile):
    results = TREEPAT.findall(infile.read())
    return [r[1] for r in results]

def get_input_tree(infile, opts=None):
    pos = infile.tell()
    line = infile.readline()
    infile.seek(pos)
    if line.upper().startswith("#NEXUS"):
        newick_trees = get_trees_from_nexus(infile)

    else:
        if opts.dsdn:
            opts.S, opts.N = map(float, infile.readline().split())
        newick_trees = infile.read().split(";")

    tree = newick.parse(newick_trees[0])
##     reroot(tree, ["ptheirospermum_tenuisec_28207", "seymeria_pectinata"])

    node, mapping = traverse(tree)
    node.sort()

    if opts.dsdn:
        def func(n):
            try:
                n.dS = n.length
                n.length = None
            except AttributeError: pass
        node.foreach(func)
        
        dN_newick = newick_trees[1].strip()
        assert dN_newick

        dN = newick.parse(dN_newick)
        labelset2treenode = tree_compare.set_labels(tree)
        labelset2dNnode = tree_compare.set_labels(dN)

        for labelset, dNnode in labelset2dNnode.items():
            treenode = labelset2treenode.get(labelset)
            if treenode:
                try:
                    gnode = mapping[treenode]
                    gnode.dN = dNnode.length
##                     gnode.dsdn = "%0.1f/%0.1f" % (gnode.dS*opts.S,
##                                                   gnode.dN*opts.N)
                    try:
                        if gnode.dN > 0.0:
                            gnode.dsdn = "%f" % (gnode.dN/gnode.dS)
                        else:
                            gnode.dsdn = ""
                    except ZeroDivisionError:
                        gnode.dsdn = ""
                except KeyError:
                    pass
        return node

    try:
        support_newick = newick_trees[1].strip()
        if support_newick:
            support = newick.parse(support_newick)
            labelset2treenode = tree_compare.set_labels(tree)
            labelset2supportnode = tree_compare.set_labels(support)

            for labelset, supportnode in labelset2supportnode.items():
                treenode = labelset2treenode.get(labelset)
                if treenode:
                    try:
                        gnode = mapping[treenode]
                        gnode.support = supportnode.length
                    except KeyError:
                        pass
    except IndexError:
        pass
        
    # add parsing for other file formats here

    return node

if __name__ == "__main__":
    main()
