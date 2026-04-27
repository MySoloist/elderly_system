import xml.etree.ElementTree as ET
import json

tree = ET.parse(r'C:\Users\asus\Desktop\wang\draw\我的流程图\订餐配送流程图_v9.drawio')
root = tree.getroot()

# 提取所有边和节点位置
edges = []
nodes = {}

for elem in root.iter('mxCell'):
    cell_id = elem.get('id', '')
    value = elem.get('value', '')
    style = elem.get('style', '')
    vertex = elem.get('vertex', '')
    edge = elem.get('edge', '')
    source = elem.get('source', '')
    target = elem.get('target', '')
    parent = elem.get('parent', '')

    geometry = elem.find('mxGeometry')
    if geometry is not None:
        x = geometry.get('x', '')
        y = geometry.get('y', '')
        width = geometry.get('width', '')
        height = geometry.get('height', '')
    else:
        x = y = width = height = ''

    if vertex == '1' and value:
        # 清理value中的HTML标签
        clean_value = value.replace('<span style="font-size: 14px;">', '').replace('</span>', '').replace('&nbsp;', ' ').strip()
        nodes[cell_id] = {
            'id': cell_id,
            'value': clean_value,
            'x': x,
            'y': y,
            'width': width,
            'height': height
        }

    if edge == '1':
        edges.append({
            'id': cell_id,
            'source': source,
            'target': target,
            'value': value,
            'parent': parent
        })

# 打印所有节点
print('=== 所有节点 ===')
for node_id in sorted(nodes.keys(), key=lambda x: int(x) if x.isdigit() else 0):
    n = nodes[node_id]
    print(f"{node_id}: {n['value'][:40]} | ({n['x']}, {n['y']})")

print('\n=== 所有连接线 ===')
for e in edges:
    src_val = nodes.get(e['source'], {}).get('value', e['source'])[:30] if e['source'] else ''
    tgt_val = nodes.get(e['target'], {}).get('value', e['target'])[:30] if e['target'] else ''
    label = f" [{e['value']}]" if e['value'] else ''
    print(f"{e['id']}: {e['source']}({src_val}) -> {e['target']}({tgt_val}){label}")

# 保存数据
with open(r'C:\Users\asus\Desktop\wang\draw\我的流程图\nodes.json', 'w', encoding='utf-8') as f:
    json.dump(nodes, f, ensure_ascii=False, indent=2)

with open(r'C:\Users\asus\Desktop\wang\draw\我的流程图\edges.json', 'w', encoding='utf-8') as f:
    json.dump(edges, f, ensure_ascii=False, indent=2)

print(f"\n共 {len(nodes)} 个节点, {len(edges)} 条边")
