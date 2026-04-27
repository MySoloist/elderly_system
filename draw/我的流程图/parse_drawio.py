import xml.etree.ElementTree as ET
import json

tree = ET.parse(r'C:\Users\asus\Desktop\wang\draw\我的流程图\订餐配送流程图_v9.drawio')
root = tree.getroot()

# 提取所有mxCell节点信息
cells = []
for elem in root.iter('mxCell'):
    cell_id = elem.get('id', '')
    value = elem.get('value', '')
    style = elem.get('style', '')
    vertex = elem.get('vertex', '')
    edge = elem.get('edge', '')
    source = elem.get('source', '')
    target = elem.get('target', '')
    parent = elem.get('parent', '')

    # 获取几何信息
    geometry = elem.find('mxGeometry')
    if geometry is not None:
        x = geometry.get('x', '')
        y = geometry.get('y', '')
        width = geometry.get('width', '')
        height = geometry.get('height', '')
    else:
        x = y = width = height = ''

    if value or style:
        cells.append({
            'id': cell_id,
            'value': value,
            'style': style,
            'vertex': vertex,
            'edge': edge,
            'source': source,
            'target': target,
            'parent': parent,
            'x': x, 'y': y, 'width': width, 'height': height
        })

# 打印所有节点
print('=== 所有节点 ===')
for c in cells:
    if c['vertex'] == '1' and c['value']:
        print(f"ID:{c['id']} | Value:{c['value'][:60]} | X:{c['x']}, Y:{c['y']}")

print('\n=== 所有连接线 ===')
for c in cells:
    if c['edge'] == '1':
        print(f"ID:{c['id']} | Source:{c['source']} -> Target:{c['target']} | Value:{c['value']}")

# 保存完整数据
with open(r'C:\Users\asus\Desktop\wang\draw\我的流程图\flowchart_data.json', 'w', encoding='utf-8') as f:
    json.dump(cells, f, ensure_ascii=False, indent=2)

print(f"\n共提取 {len(cells)} 个元素")
