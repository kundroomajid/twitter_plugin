#  Copyright (c) MAK 2021
#  Author : Kundroo Majid
#  Date : 28/04/2021

from airflow.exceptions import AirflowException
from airflow import configuration
from airflow.hooks.base_hook import BaseHook
from airflow.operators.bash_operator import BaseOperator
from airflow.models import Variable
import os,json, requests
from ExtractTable import ExtractTable

class TwitterETLOperator(BaseOperator):

    DIR_BACKUP_PATH = configuration.get_airflow_home() + '/data/'

    """
        Gets media bullitin image from twitter using url stored in 'bulliten_tweet' variable . 
       Processes the image and converts into a csv file 
    :param bulliten_tweet:      Bulliten tweet details (An Airflow Variable)
    :type bulliten_tweet: str
     :param extract_table_conn:   API key for ExtractTable libary (An Airflow Connection)
    :type bulliten_tweet: str
    """

    def __init__(self,
                 bulliten_tweet,
                 extract_table_conn,
                 bulliten_tweet_id = None,
                 bulliten_tweet_date = None,
                 bulliten_tweet_media = None,
                 *args,
                 **kwargs):

        super().__init__(*args, **kwargs)

        self.bulliten_tweet = bulliten_tweet
        self.bulliten_tweet_id = bulliten_tweet_id
        self.bulliten_tweet_date = bulliten_tweet_date
        self.bulliten_tweet_media = bulliten_tweet_media
        self.extract_table_conn = extract_table_conn

    def _check_bulliten_tweet_variable(self,context):
        """This method checks if the bulliten variable (an airflow variable) is avalaible or not
        and also checks if it is of proper format
        """
        try:
            bulliten_tweet_var = json.loads(Variable.get(self.bulliten_tweet))

            try:
                self.bulliten_tweet_id = bulliten_tweet_var['tweet_id']
            except KeyError as ke:
                raise AirflowException('Missing tweet_id in bulliten_tweet variable')
            try:
                self.bulliten_tweet_date = bulliten_tweet_var['tweet_date']
            except KeyError as ke:
                raise AirflowException('Missing tweet_date in bulliten_tweet variable')
            try:
                self.bulliten_tweet_media = bulliten_tweet_var['media_url']
            except KeyError as ke:
                raise AirflowException('Missing media_url in bulliten_tweet variable')

        except KeyError as e:
            raise AirflowException('Missing bulliten_tweet variable in Airflow Variables')

        return True

    def _get_image_from_twitter(self,context):
        url = self.bulliten_tweet_media + '?format=jpg&name=large'

        if not os.path.exists(self.DIR_BACKUP_PATH):
            os.mkdir(self.DIR_BACKUP_PATH)

        self.CURR_DATE_PATH = os.path.join(self.DIR_BACKUP_PATH, self.bulliten_tweet_date)

        if not os.path.exists(self.CURR_DATE_PATH):
            os.mkdir(self.CURR_DATE_PATH)

        try:
            response = requests.get(url)
            file = open(os.path.join(self.CURR_DATE_PATH, 'image.jpg'), "wb")
            file.write(response.content)
            file.close()
        except Exception as e:
            print("Exception|", e, "|", url)

    def _transform_image_to_df(self,context):
        #get conn variable
        try:
            conn_extract_table = BaseHook.get_connection(self.extract_table_conn)
            extract_table_api = conn_extract_table.password
        except AirflowException as e:
            raise AirflowException('Extract table connection not found')

        et_sess = ExtractTable(extract_table_api)
        usage = et_sess.check_usage()
        print(usage)
        TODAY_IMAGE_PATH = os.path.join(self.CURR_DATE_PATH, 'image.jpg')

        if os.path.exists(TODAY_IMAGE_PATH):
            data = et_sess.process_file(filepath=TODAY_IMAGE_PATH, output_format="df")
            self.data = data[0]
            return self.data
        else:
            print("Image Not Found")

    def _preprocess_df_and_save(self,context):
        if (not self.data.empty):
            header_row = 0
            self.data.columns = self.data.iloc[header_row]
            self.data = self.data.drop(header_row)
            # extract date
            date = [itm[0] for itm in self.data.columns.str.findall("([0-9]{2}\-[0-9]{2}\-[0-9]{4})") if len(itm) > 0]
            print("Date : {} ".format(date))
            date = date[0]
            # reset coulumns
            self.data.columns = self.data.iloc[1]
            self.data = self.data.reset_index(drop=True)
            self.data = self.data.drop(0)
            self.data = self.data.drop(1)
            self.data = self.data.drop(2)
            self.data = self.data.reset_index(drop=True)
            # replace few column headings
            self.data.columns.values[2] = 'Postive Today Travellers'
            self.data.columns.values[3] = 'Postive Today Others'
            self.data.columns.values[4] = 'Postive Today Total'
            self.data.columns.values[5] = 'Postive Cumulative Travellers'
            self.data.columns.values[6] = 'Postive Cumulative Others'
            self.data.columns.values[7] = 'Postive Cumulative Total'
            self.data.columns.values[8] = 'Postive Active'
            self.data.columns.values[9] = 'Recovered Today'
            self.data.columns.values[10] = 'Recovered Cumulative'

            self.data = self.data.drop(columns="S. No.")

            self.data['District'][0] = "Srinagar"
            self.data['District'][1] = "Baramulla"
            self.data['District'][2] = "Budgam"
            self.data['District'][3] = "Pulwama"
            self.data['District'][4] = "Kupwara"
            self.data['District'][5] = "Anantnag"
            self.data['District'][6] = "Bandipora"
            self.data['District'][7] = "Ganderbal"
            self.data['District'][8] = "Kulgam"
            self.data['District'][9] = "Shopain"
            self.data['District'][10] = "Kashmir Division"
            self.data['District'][11] = "Jammu"
            self.data['District'][12] = "Udhampur"
            self.data['District'][13] = "Rajouri"
            self.data['District'][14] = "Doda"
            self.data['District'][15] = "Kathua"
            self.data['District'][16] = "Samba"
            self.data['District'][17] = "Kishtwar"
            self.data['District'][18] = "Poonch"
            self.data['District'][19] = "Ramban"
            self.data['District'][20] = "Reasi"
            self.data['District'][21] = "Jammu Division"
            self.data['District'][22] = "Jammu & Kashmir"

            file_name = str(date) + '_processed.csv'
            self.data.to_csv(os.path.join(self.CURR_DATE_PATH, file_name))
            print("Processed file saved to :{}".format(os.path.join(self.CURR_DATE_PATH,file_name)))

            config = json.loads(Variable.get('config'))
            config["since_id"] = self.bulliten_tweet_id
            Variable.set("config",json.dumps(config))



    def execute(self,context):
        self._check_bulliten_tweet_variable(context)
        self._get_image_from_twitter(context)
        self._transform_image_to_df(context)
        self._preprocess_df_and_save(context)



