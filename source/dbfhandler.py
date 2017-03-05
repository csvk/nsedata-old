from dbfread import DBF

def dbf_to_csv(file):

    key_count = 0
    csv_records = []
    for rec in DBF(file):
        if key_count == 0:
            hdr = [item for item, info in rec.items()]
            hdr = ','.join(hdr)
            key_count += 1
            csv_records.append(hdr)
        data = [str(info) for item, info in rec.items()]
        data = ','.join(data)
        csv_records.append('\n{}'.format(data))
        
    return csv_records







