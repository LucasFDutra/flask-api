import os


def test():
    os.environ['PROJECT_ENVIRONMENT'] = 'TEST'
    os.system("""
        python3 flask-api/mugrations.py --up_all --test &&
        pytest --cov=./flask-api/src --cov-report=xml &&
        python3 flask-api/mugrations.py --down_all --test
    """)
