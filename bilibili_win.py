import requests
import hashlib

nodes = 'https://api.justyy.com'


def get_winners(min_n, max_n, num_win, block_num,notin):
    data = {"jsonrpc": "2.0", "method": "condenser_api.get_block", "params": [block_num], "id": 1}
    r = requests.post(url=nodes, json=data)
    rjson = r.json()
    transaction_ids = rjson["result"]['transaction_ids']
    hash = ""
    for i in transaction_ids:
        hash += i
    print(hash)
    res = hash
    winners = set()
    while len(winners) < num_win:
        res = hashlib.sha256(res.encode('utf-8')).hexdigest()
        lucky=int(res, 16) % (max_n-min_n+1) + min_n
        if lucky in notin:
            continue
        else:
            winners.add(lucky)
    return winners


open_block=95880684#开奖区块号,北京时间2025.5.26--00:00
min_lucky_number=1#最小奖卷号
max_lucky_number=181#最大奖卷号
max_lucky=1#中奖人数
#notin=[41,24, 26, 2, 13,34, 3, 52, 55, 53, 23, 21, 57, 58, 31]#已中奖排除
notin=[]
winners=get_winners(min_lucky_number,max_lucky_number,max_lucky,open_block,notin)
print(winners)
