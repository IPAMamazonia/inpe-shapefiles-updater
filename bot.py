# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from src.utils.file_path_constants import SHAPEFILES_DOWNLOAD_PATH, get_zip_file_path, generate_file_name
from src.utils.file_manager import remove_folder_and_shapeFiles, delete_and_create_folder, extract_zip
from src.db.model import DB_Model
from subprocess import call
from src.db.configs import TERMINAL_COMMAND, TABLE_NAME
import time
import os
from src.utils.ipam_slack_notifier import SlackBOT


class Bot:
    dropDown_block = [
        {'SELECTOR_ID': 'countries-export', 'OPTION': 'Brasil'},
        {'SELECTOR_ID': 'states-export', 'OPTION': 'Amazônia Legal'},
        {'SELECTOR_ID': 'filter-satellite-export', 'OPTION': 'Refer. (AQUA_M-T)'},
        {'SELECTOR_ID': 'filter-biome-export', 'OPTION': 'TODOS'},
        {'SELECTOR_ID': 'exportation-type', 'OPTION': 'Shapefile'}
        ]

    def __init__(self):
        # os.environ['MOZ_HEADLESS'] = '1'

        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2) # custom location
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir',
                               SHAPEFILES_DOWNLOAD_PATH)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')
        self.session = webdriver.Firefox(
            profile)
        
    def routine(self):
        
        try:
            exportar_dados_button = self.session.find_element_by_xpath('//*[@class="fa fa-download"]')
            exportar_dados_button.click()
            self.click_at_the_option()

            export_button = self.session.find_element_by_xpath('//*[@value="Exportar"]')
            export_button.click()
            while not os.path.exists(SHAPEFILES_DOWNLOAD_PATH):
                time.sleep(1)
        
            self.upload_files_to_db()

                                
        except NoSuchElementException:
            # SlackBOT().send_msg('[-] Ocorreu um erro. :-1:', '#inpe')
            return False

    def upload_files_to_db(self):

        db = DB_Model()
        extract_zip(get_zip_file_path())

        if db.check_if_table_exists():
            db.drop_table()

        call(TERMINAL_COMMAND.format(SHAPEFILES_DOWNLOAD_PATH,
                                        generate_file_name(), TABLE_NAME), shell=True)
        db.database_calculate_and_drop_table()

        SlackBOT().send_msg('[+] Inpe shapefile atualizado :+1: '+os.listdir(SHAPEFILES_DOWNLOAD_PATH)[0], '#inpe')
        remove_folder_and_shapeFiles() 

    def click_at_the_option(self, ):
        for dropdown_object in self.dropDown_block:
            selector = self.session.find_element_by_xpath(
                '//select[@id="'+dropdown_object['SELECTOR_ID']+'"]')
            selector.click()
            options = self.session.execute_script(
                self.js_get_options(dropdown_object['OPTION'], dropdown_object['SELECTOR_ID']))
            #selecionar paises
            self.key_navigation_routine(options, selector)
    
    def key_navigation_routine(self, options_quantitie, selector_xpath):
        for i in range(options_quantitie['option_len']):
            print i
            time.sleep(.1)
            selector_xpath.send_keys(Keys.ARROW_UP)
        time.sleep(1)
        for i in range(options_quantitie['option_index']):
            print i 
            time.sleep(.1)
            selector_xpath.send_keys(Keys.ARROW_DOWN)

    def js_get_options(self, opt_value, selector_id):
        return  ''' 
        opt = document.getElementById("'''+selector_id+'''").options
        opt_len = document.getElementById("'''+selector_id+'''").options.length

        return {'option_index': get_index_bySelectList(opt),
            'option_len' : opt_len}

        function get_index_bySelectList(opt_list){
            for( i=0; i<opt_list.length;i++){
                if(opt_list[i].text.toLowerCase() == \''''+opt_value+'''\'.toLowerCase()){
                    return i;
                }
            }    
        }

        '''


    def gotoPage(self):
        try:
            self.session.get('https://prodwww-queimadas.dgi.inpe.br/bdqueimadas/')
            self.routine()
            self.session.quit()
        except:
            SlackBOT().send_msg('[-] Ocorreu um erro. :-1:', '#inpe')

bot = Bot()
bot.gotoPage()
