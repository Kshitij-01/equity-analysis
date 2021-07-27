import json

file = (open(r"C:\Users\kshit\Desktop\edge.txt", 'r').read().split('\n'))
file.pop(-1)
print(len(file))
file = [file[-1]]
ring = "    {} = models.CharField(max_length=50)"

for f in file:
    jj = json.loads(str(f))
    for j in jj[-1]:
        if isinstance(j, dict):
            for i, p in j.items():
                if i.startswith('r') or i.startswith('p'):
                    print("class {}_ticker(models.Model):".format(
                        i.replace('row headers ', '').strip().replace('&', 'and').replace('.', '').replace(' ',
                                                                                                           '_').strip(
                            '_').replace('/',
                                         '').replace(
                            '(', '').replace(')', '').replace('-', '_').replace('%', '').replace("'", "").replace('9_',
                                                                                                                  '').strip('_').replace('__','_')))
                    for x in p:
                        print(ring.format(
                            x.strip().strip().replace('&', 'and').replace('.', '').replace(' ', '_').strip('_').replace(
                                '/',
                                '').replace(
                                '(', '').replace(')', '').replace('-', '_').replace('%', '').replace("'", "").replace(
                                '9_', '').strip('_').replace('__','_')))
                    print('')
    print(' now stock edge')
    for j in jj[:-3]:
        if isinstance(j, dict):
            for t, y in j.items():
                print("class {}_stockedge(models.Model):".format(
                    y.strip().replace('&', 'and').replace('.', '').replace(' ', '_').replace('/',
                                                                                                        '').replace(
                        '(', '').replace(')', '').replace('-', '_').replace('%', '').replace("'", "").replace('9_',
                                                                                                              '').strip('_').replace('__','_')))
                break
            li = []
            for t, y in j.items():
                li.append(t.strip())
            # print(t.strip(), end=" ")

            for x in li:
                print(ring.format(
                    x.strip().replace('&', 'and').replace('.', '').replace(' ', '_').strip('_').replace('/',
                                                                                                        '').replace(
                        '(', '').replace(')', '').replace('-', '_').replace("'", "").replace('%', '').replace('9_',
                                                                                                              '').strip('_').replace('__','_')))
            print('')
    for f, g in jj[-3].items():
        print(f, g)

    print(
        '---------------------------------------------------------------------------------------------------------------')
# break
