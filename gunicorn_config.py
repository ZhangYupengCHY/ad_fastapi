# ������
workers = 2
# ÿ�����̵��߳���
threads = 4
# �˿�5000
bind = '0.0.0.0:8040'
# ����ģʽЭ��
worker_class = 'gevent'
# ��󲢷���
worker_connections = 100
# ����pid�ļ�
pidfile = 'gunicorn.pid'
# ������־�ʹ�����Ϣ��־��·��
# ��־��¼����
loglevel = 'info'
# ���뷢���仯�Ƿ��Զ�����
reload = True