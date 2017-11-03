# encoding: UTF-8

from jaqs.util import fileio
from jaqs.trade.tradeapi import TradeApi

def test_trade_api():
    dic = fileio.read_json(fileio.join_relative_path('etc/trade_config.json'))
    address = dic.get("remote.address", None)
    username = dic.get("remote.username", None)
    password = dic.get("remote.password", None)
    if address is None or username is None or password is None:
        raise ValueError("no trade service config available!")
    
    tapi = TradeApi(address, prod_type='jaqs')

    # TradeApiͨ���ص�������ʽ֪ͨ�û��¼����¼��������֣�����״̬���ɽ��ر���ί������ִ��״̬��

    # ����״̬����
    def on_orderstatus(order):
        print "on_orderstatus:" #, order
        for key in order:    print "%20s : %s" % (key, str(order[key]))
        print ""


    # �ɽ��ر�����
    def on_trade(trade):
        print "on_trade:"
        for key in trade:    print "%20s : %s" % (key, str(trade[key]))
        print ""

    # ί������ִ��״̬����
    # ͨ�����Ժ��Ըûص�����
    def on_taskstatus(task):
        print "on_taskstatus:"
        for key in task:    print "%20s : %s" % (key, str(task[key]))
        print ""

    tapi.set_ordstatus_callback(on_orderstatus)
    tapi.set_trade_callback(on_trade)
    tapi.set_task_callback(on_taskstatus)
    
    # ʹ���û����������½�� ����ɹ��������û����õĲ����ʺ��б�
    user_info, msg = tapi.login(username, password)
    print "msg: ", msg
    print "user_info:", user_info

    # ѡ��ʹ�õĲ����ʺ�
    #
    # �ú����ɹ����µ�����ֲֵȺͲ����ʺ��йصĲ������͸ò����ʺŰ󶨡�
    # û�б�Ҫÿ���µ�����ѯ�����øú������ظ����øú�������ѡ���µĲ����ʺš�
    #
    # ����ɹ�������(strategy_id, msg)
    # ���򷵻� (0, err_msg)
    sid, msg = tapi.use_strategy(9111)
    print "msg: ", msg
    print "sid: ", sid    

    # ��ѯPortfolio
    #
    # ���ص�ǰ�Ĳ����ʺŵ�Universe�����б�ĵľ��ֲ֣������ֲ�Ϊ0�ı�ġ�

    df, msg = tapi.query_account()
    print "msg: ", msg
    df    
    
    # ��ѯ��ǰ�����ʺŵ����гֲ�
    #
    # �� query_portfolio�ӿڲ�һ�������Ī���ڻ���Լ Long, Short���������гֲ֣������Ƿ���������¼
    # ���ص� size ��������ȫ��Ϊ ��
    df, msg = tapi.query_position()
    print "msg: ", msg
    df

    # �µ��ӿ�
    #  (task_id, msg) = place_order(code, action, price, size )
    #   action:  Buy, Short, Cover, Sell, CoverToday, CoverYesterday, SellToday, SellYesterday
    # ���� task_id �����ø� task_id
    task_id, msg = tapi.place_order("000025.SZ", "Buy", 57, 100)
    print "msg:", msg
    print "task_id:", task_id

    # ��ѯPortfolio
    #
    # ���ص�ǰ�Ĳ����ʺŵ�Universe�����б�ĵľ��ֲ֣������ֲ�Ϊ0�ı�ġ�

    df, msg = tapi.query_portfolio()
    print "msg: ", msg
    df

    # �����µ�1��place_batch_order
    #
    # ����task_id, msg��
    orders = [ 
        {"security":"600030.SH", "action" : "Buy", "price": 16, "size":1000},
        {"security":"600519.SH", "action" : "Buy", "price": 320, "size":1000},
        ]

    task_id, msg = tapi.place_batch_order(orders, "", "{}")
    print task_id
    print msg    

    # cancel_order
    # ����
    tapi.cancel_order(task_id)

    # �����µ�2��basket_order
    #
    # ����task_id, msg��
	orders = [ 
		{"security":"TF1706.CFE", "ref_price": 98.240, "inc_size":10},
		{"security":"T1706.CFE",  "ref_price": 95.540, "inc_size":-17},
		]

	task_id, msg = tapi.basket_order(orders, "", "{}")
	print task_id
	print msg

    #  goal_protfolio
    #  ������Ŀ��ֲ�
    #  ���أ�(result, msg)
    #     result:  �ɹ���ʧ��
    #     msg:     ����ԭ��
    #  ע�⣺Ŀ��ֲ��б���������еĴ���ĳֲ֣���ʹ���޸�
    
    # �Ȳ�ѯ��ǰ�ĳֲ�, 
    portfolio = ts.query_portfolio()
    
    goal = pd.DataFrame(portfolio['size'])
    goal['refpx'] = 0.0
    goal['urgency'] = 10

    #  Ȼ���޸�Ŀ��ֲ�
    code = '150131.SZ'
    goal['ref_price'][code] = 0.630
    goal['size'][code] -= 20000

    code = 'IF1712.CFE'
    goal['refpx'][code] = 4000.2
    goal['size'][code] -= 1

    # ��������
    result, msg = ts.goal_portfolio(goal)
    print result, msg
	
	# stop_portfolio
    # ����, ��������portfolio����
	tapi.stop_portfolio()

    
if __name__ == "__main__":
    test_trade_api()
