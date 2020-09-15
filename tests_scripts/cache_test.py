
from krakenschema.cache import Cache
from krakenschema.schema import Schema


class Tests:
    def test_post(self):
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


    def test_replace_value(self):

        input_record = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': {
                'key31': 'value31',
                'key32': 'value32'
            },
            'key4': [
                {'key41': 'value41'},
                {'key42': 'value42'}
            ]

        }

        expected_record = {
                        'key1': 'value1',
            'key2': 'value2',
            'key3': {
                'key31': 'value31',
                'key32': 'valueNEW',
            },
            'key4': [
                {'key41': 'value41'},
                {'key42': 'value42'}
            ]

        }

        schema = Schema()
        output_record = schema.replace_value(input_record, 'key32', 'value32', 'valueNEW' )

        if output_record == expected_record:
            print('pass')
        else: 
                print('fail')
                print(output_record)