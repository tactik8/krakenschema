
import re

from krakenhelper.helper import Url, Date, UUID


class Schema:
    def __init__(self, record_type = None, record_id = None, record = None):
        self.record_type = record_type
        self.record_id = record_id
        self.record = record
        self.metadata = None


        self.main_record = None
        self.record_list = None

        self.valid = None
        self.ref_id = None
    
    def _get_record_type(self):
        if self.record:
            if isinstance(self.record, dict):
                self.record_type = self.record.get('@type', None)

        return self.record_type


    def _get_record_id(self):
        if self.record:
            if isinstance(self.record, dict):
                self.record_id = self.record.get('@id', None)

        
        # Assign from record_type if exist
        if not self.record_id:
            if self.record_type == 'schema:website':
                self.record_id = self.get_url_id()
            
            elif self.record_type == 'schema:webpage':
                self.record_id = self.get_url_id()
            
            elif self.record_type == 'schema:videoobject':
                self.record_id = self.get_contenturl_id()
            
            elif self.record_type == 'schema:imageobject':
                self.record_id = self.get_contenturl_id()

            elif self.record_type == 'schema:person':
                self.record_id = self.get_email()

            elif self.record_type == 'schema:organization':
                self.record_id = self.get_domain()

        return self.record_id


    def get(self):


        return self.record


    def post(self, record = None): 

        if record:
            self.record = record


        record, record_list = self.get_main_record()


        record_id_map = {}
        for i in record_list:
            sub_record = Schema()

            
            sub_record._post_item(i)




        # Verify if record is valid
        if not self.get_valid():
            return None

        # Search for record if no id
        if not self.record_id:
            self.search_record_id()


        # Retrieve record
        if self.record_id:
            ref_record = Schema(self.record_type, self.record_id)
            ref_record.get()



        # Assign uuid if no id
        if not self.record_id:
            u = UUID()
            self.record_id = u.get()
        

        return self.record_id

    def _post_item(self):

        # Verify if record is valid
        if not self.get_valid():
            return None

        # Search for record if no id
        if not self.record_id:
            self.search_record_id()


        # Retrieve record
        if self.record_id:
            ref_record = Schema(self.record_type, self.record_id)
            ref_record.get()


        # Assign uuid if no id
        if not self.record_id:
            u = UUID()
            self.record_id = u.get()




    def pre_processing(self): 

        if not self.record_id:
            self.search_record_id()

        if not self.record_id:
            u = UUID()
            self.record_id = u.get()




    def get_valid(self, record = None):
        """
        Check if schema is valid

        Parameters
        ----------
        record (dict): The record to check

        Returns
        -------
        bool : True if valid schema
        """

        if record:
            self.record = record

        self._get_record_type()

        if self.record_type:
            self.valid = True
        else:
            self.valid = False

        return self.valid


    def get_ref_id(self, record = None):
        """
        Get the ref_id of a record, the shorthand notation

        Parameters
        ----------
        record (dict): The record

        Returns
        -------
        dict : A ref_id dict or None if invalid
        """

        if record:
            self.record = record
        
        # Process record
        self._get_record_type()
        self._get_record_id()

        # Error handling
        if self.get_valid() == False:
            return None

        if not self.record_type or not self.record_id:
            return None


        # Get ref_id
        self.ref_id = {
            '@type': self.record_type,
            '@id': self.record_id
            }

        return self.ref_id


    def search_record_id(self):
        # Search record in database if exist, returns record-id if so

        return self.record_id


    def get_main_record(self, record = None):
        """
        Repleaces sub_records with their ref_id reference, returning a simpler record

        Parameters
        ----------
        record (dict): The record

        Returns
        -------
        dict : A simplified record with ref_if for sub records
        """

        if record:
            self.record = record

        # Error handling
        if not self.record or not isinstance(self.record, dict):
            return None

        # Initialize record list
        self.record_list = []


        def _process_dict(record, parent):

            if not record.get('@type', None):
                return record

            
            # Assign itself as parent
            schema = Schema()
            record_ref_id = schema.get_ref_id(record)
            
            # Assign temp id if no record_id
            if not schema.record_id:
                u = UUID()
                schema.record_id = 'temp' + u.get()
                record_ref_id = schema.get_ref_id()


            # Iterate through keys
            new_record = {}
            for key in record:
                new_record[key] = _process_record(record[key], record_ref_id)

            # If parent exist, assign parent to record and return ref_id
            if parent and record_ref_id: 
                # assign parent record
                parent_schema = Schema()
                new_record['kraken:parent'] = parent_schema.get_ref_id(parent)
                
                # Add to record list
                self.record_list.append(new_record)

                # Return
                print('rec', record_ref_id)
                return record_ref_id

            else:
                # Return record
                self.record_list.append(new_record)
                return new_record


        def _process_list(record, parent):
            new_record = []
            for i in record:
                new_record.append(_process_record(i, parent))
            return new_record


        def _process_record(record, parent = None):
            
            if isinstance(record, str):
                new_record = record

            elif isinstance(record, dict):
                new_record =  _process_dict(record, parent)
            
            elif isinstance(self.record, list):
                new_record = _process_list(record, parent)

            else:
                new_record = record


            return new_record


        self.main_record = _process_record(self.record)
        return self.main_record, self.record_list




    def flatten_schema(self, record):
        record, record_list = self._process_schema(record, keep=False, temp_id = True)




    def _process_schema(self, record, keep=True, temp_id = True):
        # Decompose nested schema record into a list 
        # if keep == False, replace sub_record by their ref_id
        # If temp_id == True, repalce mepty @id by a temp one

        # Operation (recursive)
        def _flatten_iterate(record, id_count = 0):
            schema_list = []
            


            if isinstance(record, dict):



                #Set temp id if none
                record_type = record.get('@type', None)
                record_id = record.get('@id', None)

                if record_type and not record_id and temp_id == True:
                    record['@id'] = '_temp_id_' + str(id_count)
                    id_count += 1


                # Iterate through keys (recursion)
                new_record = {}
                for i in record:
                    
                    sub_record, sub_list = _flatten_iterate(record[i], id_count)
                    
                    if sub_list:
                        schema_list += sub_list
                    if self.schema_test_valid(sub_record) == True:
                        if keep == True:
                            new_record[i] = sub_record
                        else:
                            new_record[i] = self.get_ref_id(sub_record) 
                    else:
                        new_record[i] = sub_record

                # Check if schema, add if so 
                if self.schema_test_valid(new_record) == True:
                    # Add record to list
                    schema_list.append(new_record)


            elif isinstance(record, list) and not isinstance(record, str):
                new_record = []
                for r in record:
                    new_sub, sub_list = _flatten_iterate(r, keep, id_count)
                    
                    if new_sub:
                        new_record.append(new_sub)
                    if sub_list:
                        schema_list += sub_list         
            else:
                a=1 # do nothing
                new_record = record

            return new_record, schema_list

        # Decompose nested schema record into a list 

        # Error handling
        # Convert to normal record if list of 1
        if isinstance(record, list) and len(record) == 1:
            record = record[0]
        # If not record
        elif not isinstance(record, dict):
            self.result = None
            self.status = False

        # Process
        record, schema_list = _flatten_iterate(record)

        self.value = record, schema_list
        return self.value


    def get_test(self):
        """
        Returns a generic test schema

        Parameters
        ----------

        Returns
        -------
        dict : A generic test schema
        """

        self.record_type = 'schema:test'
        self.record_id = 'generic id'
        self.record = { 
            '@type': self.record_type,
            '@id': self.record_id,
            'schema:name': 'Test record',
            'schema:url': 'https://www.test.com',
            'schema:address': {
                '@type': 'schema:postaladdress',
                'schema:streetaddress': '269 de Carignan',
                'schema:address:locality': 'Repentigny',
                'schema:addresscountry': 'CA',
                'schema:postalcode': 'J5Y4A9'
            },
            'schema:contactpoint': [
                {
                    '@type': 'schema:contactpoint',
                    'schema:email': 'test@test.com'
                },
                {
                    '@type': 'schema:contactpoint',
                    'schema:email': 'test2@test2.com'
                }
            ]
        }
        return self.record


    def get_url(self):
        return self.record.get('schema:contenturl', None)

    def get_url_id(self):
        ### give web safe url for id purposes

        self.record_id = self.get_url()

        if self.record_id:
            self.record_id = self.record_id.replace("https://", "")
            self.record_id = self.record_id.replace("http://", "")
            self.record_id = self.record_id.replace("www.", "")
            self.record_id = self.record_id.rstrip("/")

            self.record_id = re.sub("[^0-9a-zA-Z]+", "_", self.record_id)

        return self.record_id



    def get_contenturl(self):
        return self.record.get('schema:contenturl', None)




    def get_contenturl_id(self):
        self.record_id = self.get_contenturl()

        if self.record_id:
            self.record_id = self.record_id.replace("https://", "")
            self.record_id = self.record_id.replace("http://", "")
            self.record_id = self.record_id.replace("www.", "")
            self.record_id = self.record_id.rstrip("/")

            self.record_id = re.sub("[^0-9a-zA-Z]+", "_", self.record_id)

        return self.record_id

    def get_domain(self):
        u = Url()
        return u.get_domain(self.get_url())


    def get_metadata(self):

        if not self.metadata:
            self._generate_metadata()
        
        return self.metadata



    def _generate_metadata(self):

        d = Date()

        datasource = self.record.get('kraken:datasource', {})
        
        # Define base metadata

        for i in self.record:
            self.metadata[i]['kraken_created_date'] = self.record.get('kraken:created_date', None)

            self.metadata[i]['kraken_modified_date'] = self.record.get('kraken:modified_date', None)
            
            self.metadata[i]['datasource_created_date'] = self.record.get('kraken:datasource_created_date', None)

            self.metadata[i]['datasource_modified_date'] = self.record.get('kraken:datasource_modified_date', None)

            self.metadata[i]['credibility'] = self.record.get('kraken:credibility', 0)

