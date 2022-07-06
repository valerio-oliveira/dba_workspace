from hashlib import new
from src.processing.SoProcessor import SoProcessor


class HostSummary:
    def process(self, host_name: str = '', get_log_list: bool = True):
        self.summary = []
        so_processor = SoProcessor()
        so_processor.process()
        for host in so_processor.facts:
            # machine_id = host[0]
            hostname = host[1]
            address = host[2]
            log_file = host[3]
            log_size = host[4].split('\t')[0]
            log_dir = host[4].split('\t')[1]
            # facts = host[5]
            # db_params = host[6]
            db_logs = host[7]
            log_line = []
            if get_log_list:
                list_log_summary = self.__get_logs_summary(db_logs)
                seq = 0
                for key, value in list_log_summary:
                    seq += 1
                    log_line.append(([seq, key, ]+value))

            if host_name == '' or host_name == hostname:
                self.summary.append(
                    [hostname, address, log_file, log_size, log_dir, log_line])

        # print('summary len', len(self.summary), 'host_name', host_name)

    def get(self):
        return tuple(self.summary)

    def __get_logs_summary(self, db_logs):
        dict_log = {}
        for item in db_logs:
            last_line = item[0]
            last_date = item[1]
            last_pid = item[2]
            last_db = item[3]
            last_user = item[4]
            last_app = item[5]
            last_ip = item[6]
            last_msg = item[7]
            line_value = dict_log.get(last_msg, [])
            if line_value:
                count = int(line_value[0]) + 1
            else:
                count = 1

            dict_log[last_msg] = [count, last_line, last_date,
                                  last_pid, last_db, last_user, last_app, last_ip]
        dict_log = self.__sort_by_index_value(dict_log, reverse=True)
        return dict_log

    def __sort_by_index_value(self, d, reverse=False):
        return sorted(d.items(), key=lambda x: x[1], reverse=reverse)
