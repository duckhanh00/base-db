import time

from app.databases.mongodb.mongodb_bricher import MongoBricher
from app.constants.mongodb_constants import MongoCollections
from app.utils.time_utils import TimeUtils
import config

class CheckBricher:
    def __init__(self):
        self.mongo_main = MongoBricher(config.MongoDBConfig.BRICHER_MAIN_URL)
        self.mongo_test = MongoBricher(config.MongoDBConfig.BRICHER_TEST_URL)

        self.main_lending_ids = self.mongo_main.get_all_id(MongoCollections.lendings)
        self.test_lending_ids = self.mongo_test.get_all_id(MongoCollections.lendings)

        self.main_borrow_ids = self.mongo_main.get_all_id(MongoCollections.borrows)
        self.test_borrow_ids = self.mongo_test.get_all_id(MongoCollections.borrows)

        self.main_vault_ids = self.mongo_main.get_all_id(MongoCollections.vaults)
        self.test_vault_ids = self.mongo_test.get_all_id(MongoCollections.vaults)



    def check_all_id(self):
        print("****")
        print("number docs lending main: ", len(self.main_lending_ids), "| number docs lending test: ", len(self.test_lending_ids))
        print("number docs borrow main: ", len(self.main_borrow_ids), "| number docs borrow main: ", len(self.test_borrow_ids))
        print("number docs vaults main: ", len(self.main_vault_ids), "| number docs vaults test: ", len(self.test_vault_ids))
        print("****")

    def check_value_roi_change_logs(self, col, ids, one, three):
        for item in ids:
            roi_main = self.mongo_main.get_roi_change_logs(col, item)
            roi_test = self.mongo_test.get_roi_change_logs(col, item)
  
            if roi_test is None:
                print("****")
                print("None roi test", item)
                print("****")
                continue

            cons = 0
            prev_time = 0
            for time in roi_test["roiChangeLogs"]:
                test = roi_test["roiChangeLogs"][time]
                if time not in roi_main["roiChangeLogs"]:
                    print("****")
                    print(f"{col} roichangelogs test co nhung main khong co")
                    print(item) 
                    print("Time: ", time)
                    print("****")
                    continue
                
                range_time = int(time) - int(prev_time)
                if range_time != cons:
                    cons = range_time
                    if cons == 3600 and prev_time != three: 
                        print("****")
                        print(item)
                        print(col, f"time: {time}", f"prev_time: {prev_time}", f"range: {range_time}",)
                        print("****")
                        return 0
                    if cons == 900 and prev_time != one: 
                        print("****")
                        print(item)
                        print(col, f"time: {time}", f"prev_time: {prev_time}", f"range: {range_time}",)
                        print("****")
                        return 0

                prev_time = int(time)
                
                main = roi_main["roiChangeLogs"][time]

                if test != main:
                    print("****")
                    print(f"Fail {col} {item}", f"Main roi {time}: {main}", f"Test roi {time}: {test}")
                    print("****")
                    return 0
        print(f"ROI CHANGE LOGS {col} OK!")


    def check_value_detail_roi_change_logs(self, col, ids, one, three):
        for item in ids:
            detail_roi_main = self.mongo_main.get_detail_roi_change_logs(col, item)
            detail_roi_test = self.mongo_test.get_detail_roi_change_logs(col, item)

            if detail_roi_test is None:
                print("****")
                print("None detail roi test", item)
                print("****")
                continue

            cons = 0
            prev_time = 0

            for time in detail_roi_test["detailROIChangeLogs"]:
                if time not in detail_roi_main["detailROIChangeLogs"]:
                    print("****")
                    print(f"{col} detailROIChangeLogs test co nhung main khong co")
                    print(item) 
                    print("Time: ", time)
                    print("****")
                    continue
                
                range_time = int(time) - int(prev_time)
                if range_time != cons:
                    cons = range_time
                    if cons == 3600 and prev_time != three: 
                        print("****")
                        print(col, f"time: {time}", f"prev_time: {prev_time}", f"range: {range_time}",)
                        print("****")
                        return 0
                    if cons == 900 and prev_time != one: 
                        print(col, f"time: {time}", f"prev_time: {prev_time}", f"range: {range_time}",)
                        return 0

                prev_time = int(time)

                main_deposit = detail_roi_main["detailROIChangeLogs"][time]['depositAPY']
                main_reward = detail_roi_main["detailROIChangeLogs"][time]['rewardDepositAPY']

                test_deposit = detail_roi_test["detailROIChangeLogs"][time]['depositAPY']
                test_reward = detail_roi_test["detailROIChangeLogs"][time]['rewardDepositAPY']

                if main_deposit != test_deposit or main_reward != test_reward:
                    print("*****")
                    print(f"Fail {col} {item}", f"Main detail roi deposit {time}: {main_deposit}", f"Test detail roi deposit {time}: {test_deposit}")
                    print(f"Fail {col} {item}", f"Main detail roi reward {time}: {main_reward}", f"Test detail roi reward {time}: {test_reward}")
                    print("*****")
                    return 0
        print(f"DETAIL ROI CHANGE LOGS {col} OK!")


    def check_value_liquidity_change_logs(self, col, ids, one, three):
        for item in ids:
            liquid_main = self.mongo_main.get_liquidity_change_logs(col, item)
            liquid_test = self.mongo_test.get_liquidity_change_logs(col, item)
  
            if liquid_test is None:
                print("****")
                print("None liquidity test", item)
                print("****")
                continue

            cons = 0
            prev_time = 0

            for time in liquid_test["liquidityChangeLogs"]:
                if time not in liquid_main["liquidityChangeLogs"]:
                    print("****")
                    print(f"{col} liquidityChangeLogs test co nhung main khong co")
                    print(item) 
                    print("Time: ", time)
                    print("****")
                    continue

                range_time = int(time) - int(prev_time)
                if range_time != cons:
                    cons = range_time
                    if cons == 3600 and prev_time != three: 
                        print("****")
                        print(item)
                        print(col, f"time: {time}", f"prev_time: {prev_time}", f"range: {range_time}",)
                        print("****")
                        return 0
                    if cons == 900 and prev_time != one: 
                        print("****")
                        print(item)
                        print(col, f"time: {time}", f"prev_time: {prev_time}", f"range: {range_time}",)
                        print("****")
                        return 0

                prev_time = int(time)
                
                main_borrow_amount = 0
                main_borrow_usd = 0
                if col == 'lendings':
                    main_borrow_amount = liquid_main["liquidityChangeLogs"][time]['totalBorrow']['amount']
                    main_borrow_usd = liquid_main["liquidityChangeLogs"][time]['totalBorrow']['valueInUSD']
                main_deposit_amount = liquid_main["liquidityChangeLogs"][time]['totalDeposit']['amount']
                main_deposit_usd = liquid_main["liquidityChangeLogs"][time]['totalDeposit']['valueInUSD']
                
                test_borrow_amount = 0
                test_borrow_usd = 0
                if col == 'lendings':
                    test_borrow_amount = liquid_test["liquidityChangeLogs"][time]['totalBorrow']['amount']
                    test_borrow_usd = liquid_test["liquidityChangeLogs"][time]['totalBorrow']['valueInUSD']
                test_deposit_amount = liquid_test["liquidityChangeLogs"][time]['totalDeposit']['amount']
                test_deposit_usd = liquid_test["liquidityChangeLogs"][time]['totalDeposit']['valueInUSD']

                if col == 'lendings' and (test_borrow_amount == 0 or test_borrow_usd == 0):
                    print(f'not borrow in {col} test {item}')
                    return 0
                if col == 'lendings' and (main_borrow_amount == 0 or main_borrow_usd == 0):
                    print(f'not borrow in {col} main {item}')
                    return 0

                if main_borrow_amount != test_borrow_amount or main_borrow_usd != test_borrow_usd or main_deposit_amount != test_deposit_amount or main_deposit_usd != test_deposit_usd:
                    print("****")
                    if col == 'lendings': 
                        print(f"Fail {col} {item}", f"Main liquid total borrow amount {time}: {main_borrow_amount}", f"Test liquid total borrow amount {time}: {test_borrow_amount}")
                        print(f"Fail {col} {item}", f"Main liquid total borrow usd {time}: {main_borrow_usd}", f"Test liquid total borrow usd {time}: {test_borrow_usd}")
                    print(f"Fail {col} {item}", f"Main liquid total deposit amount {time}: {main_deposit_amount}", f"Test liquid total deposit amount {time}: {test_deposit_amount}")
                    print(f"Fail {col} {item}", f"Main liquid total deposit usd {time}: {main_deposit_usd}", f"Test liquid test {time}: {test_deposit_usd}")
                    print("****")
                    return 0

        print(f"LIQUIDITY CHANGE LOGS {col} OK!")
    

    def check_all(self):
        last_month = time.time() - 86400*32
        three_month_ago = time.time() - 86400*92

        one = TimeUtils.round_timestamp(last_month, 86400)
        three = TimeUtils.round_timestamp(three_month_ago, 86400)
        print('THREE MONTH AGO:', three)
        print('ONE MONTH AGO:', one)
        
        
        self.check_value_roi_change_logs(MongoCollections.lendings, self.main_lending_ids, one, three) 
        self.check_value_roi_change_logs(MongoCollections.borrows, self.main_borrow_ids, one, three)
        self.check_value_roi_change_logs(MongoCollections.vaults, self.main_vault_ids, one, three)

        self.check_value_detail_roi_change_logs(MongoCollections.lendings, self.main_lending_ids, one, three) 
        self.check_value_detail_roi_change_logs(MongoCollections.borrows, self.main_borrow_ids, one, three)

        self.check_value_liquidity_change_logs(MongoCollections.lendings, self.main_lending_ids, one, three)
        self.check_value_liquidity_change_logs(MongoCollections.vaults, self.main_vault_ids, one, three)

