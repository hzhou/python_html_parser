import re
def test():
    f = open('test.html')
    s = f.read()
    root_node = parse_html(s)
    print("root_node: ", type(root_node), "\n")
    debug_dom(root_node)

def parse_html(s):
    tag_stack=[]
    cur_list=[]
    tag_stack.append({'_name':'root', '_list':cur_list})
    debug_dom(tag_stack[0])
    n=len(s)
    i=0
    while i<n:
        m = re.match(r"<!--.*-->", s[i:])
        if m:
            i+=m.end()
            continue
        m = re.match(r"<!DOCTYPE.*>", s[i:])
        if m:
            i+=m.end()
            continue
        m = re.match(r"[^<]+", s[i:])
        if m:
            i+=m.end()
            cur_list.append(m.group(0))
            continue
        m = re.match(r"<(\w+)(.*?)>", s[i:])
        if m:
            i+=m.end()
            s_name=m.group(1)
            s_attr=m.group(2)
            tag = {'_name':s_name}
            parse_attribute(tag, s_attr)
            cur_list.append(tag)
            if '/' in tag or re.match(r"area|base|br|col|embed|hr|img|input|keygen|link|meta|param|source|track|wbr", s_name):
                pass
            elif re.match(r"script|style|textarea|title", s_name):
                i_start=i
                while i<n:
                    m = re.match(r"([^<]|<[^/])+", s[i:])
                    if m:
                        i+=m.end()
                        continue
                    m = re.match(r"</(\w+).*?>", s[i:])
                    if m:
                        i+=m.end()
                        if m.group(1)==s_name:
                            break
                        else:
                            continue
                    i+=1
                i_end=i
                tag['_text'] = s[i_start:i_end]
            else :
                tag_stack.append(tag)
                cur_list=[]
                tag['_list'] = cur_list
            continue
        m = re.match(r"</(\w+).*?>", s[i:])
        if m:
            i+=m.end()
            s_name=m.group(1)
            if s_name == tag_stack[-1]['_name']:
                tag_stack.pop()
                cur_list=tag_stack[-1]['_list']
            else:
                j=len(tag_stack)-2
                while j>0:
                    if s_name == tag_stack[j]['_name']:
                        while len(tag_stack)>=j:
                            tag_stack.pop()
                        cur_list=tag_stack[-1]['_list']
                        break
                    j-=1
            continue
        i+=1
    return tag_stack[0]

def parse_attribute(tag, s_attr):
    n=len(s_attr)
    i=0
    while i<n:
        m = re.match(r"\s+", s_attr[i:])
        if m:
            i+=m.end()
            continue
        m = re.match(r"/", s_attr[i:])
        if m:
            i+=m.end()
            tag['/']=1
            continue
        m = re.match(r"([^\s'\"\\=<>`]+)", s_attr[i:])
        if m:
            i+=m.end()
            s_attr_name=m.group(1)
            m = re.match(r"\s*=\s*", s_attr[i:])
            if m:
                i+=m.end()
                while i<n:
                    m = re.match(r"\"((?:[^\\\"]+|\\.)*)\"", s_attr[i:])
                    if m:
                        i+=m.end()
                        tag[s_attr_name] = m.group(1)
                        break
                    m = re.match(r"'((?:[^\\\']+|\\.)*)'", s_attr[i:])
                    if m:
                        i+=m.end()
                        tag[s_attr_name] = m.group(1)
                        break
                    m = re.match(r"[^\s'\"=<>`]+", s_attr[i:])
                    if m:
                        i+=m.end()
                        tag[s_attr_name] = m.group(0)
                        break
                    i+=1
            else:
                tag[s_attr_name]=1
            continue

def debug_dom(node):
    def print_node(node, level):
        if isinstance(node, str):
            print("    " * level, node)
        else:
            print("    " * level, node['_name'])
            if "_list" in node:
                for t in node['_list']:
                    print_node(t, level+1)
    print_node(node, 0)

test()