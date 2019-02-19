import itertools
import dedupe
from baselinededupe import models
def blockingsql(deduper):
    aall = models.blocking_map.objects.all()
    aall.delete()
    print('creating inverted index')
    for field in deduper.blocker.index_fields:
        print(field)
