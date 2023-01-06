from django.core.management.base import BaseCommand
from api.models import User
from faker import Faker
from tqdm import tqdm
import pandas as pd
from joblib import Parallel, delayed
f = Faker()


def generate_data(x):
    name = f.first_name()
    
    return [x, name, name[:4], f.last_name(), f.email(), f.password()]

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

class Command(BaseCommand):
    help = 'run this in order to download the vault file'
    def handle(self, *args, **kwargs):
        print('Running')
        user_ids = []
        # number = 1,000,000,000
        number = 100000000 
        number = 100000
        # print(number // 2000)

        # for x in range(number // 2000):
        names = Parallel(n_jobs=1024, backend='threading')(delayed(generate_data)(z) for z in tqdm(range(number)))
        df = pd.DataFrame(names)
        df.columns = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        df['is_active'] = True
        df.to_csv('test.csv', index=False)
            # print(names)
            # User.objects.bulk_create(names)
        # ranges = list(split(range(number), number//3000))
        # print('Number of ranges', ranges)
        # number = 100
        # _ = Parallel(n_jobs=64, backend='threading')(delayed(generate_data)(x) for x in tqdm(range(number)))
        # print(names)
        # for _ in tqdm(range(number)):
        #     name = f.first_name()
        #     user = User.objects.create(
        #      username = name,
        #      first_name= name[:4],
        #      last_name=f.last_name(),
        #      email = f.email(),
        #      password = f.password()
        #     )
        #     # user.save()
        #     user_ids.append(user)
        
       