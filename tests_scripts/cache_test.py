
from kraken_schema.cache import Cache
from kraken_schema.schema import Schema


class Tests:
    def test_post():
        cache = Cache()

        schema = Schema()
        input_record = schema.get_test()
        input_record_type = input_record.get('@type', None)
        input_record_id = input_record.get('@id', None)

        cache.post(input_record)
        output_record = cache.get(input_record_type, input_record_id)

        if input_record == output_record:
            print('pass')
        else: 
            print('fail')

