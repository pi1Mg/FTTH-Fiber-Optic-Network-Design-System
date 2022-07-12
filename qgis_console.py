fts = list(iface.mapCanvas().currentLayer().getFeatures())

inss = list()
for i in fts:
    for j in fts:
        if i.geometry().intersects(j.geometry()):
            ins = i.geometry().intersection(j.geometry())
            inss.append(ins)