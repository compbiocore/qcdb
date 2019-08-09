from qcdb.parsers.parse import BaseParser
import json, logging, os, glob2, re

log = logging.getLogger(__name__)
dirname = os.path.dirname('__file__')

class picardtoolsParser(BaseParser):

    def __init__(self, file_handle, session, ref_table, build_ref):
        log.info("Initializing picardtoolsParser...")
        BaseParser.__init__(self,file_handle,'picard', session, ref_table, build_ref)
        file_table_dict = {'insertsize_metrics_picard': 'insertsizemetrics',
            'alignment_summary_metrics_picard': 'alignmentmetrics',
            'summary_gcbias_metrics_picard': 'gcbiasmetrics'}

        base_file = os.path.basename(file_handle)
        if self.library_read_type == 'single ended':
            file_type = base_file.split('{}_{}_'.format(self.sample_id,self.experiment))[1]
        else:
            file_type = base_file.split('{}_{}_?_'.format(self.sample_id,self.experiment))[1]
        metric = file_table_dict[file_type[:-4]]

        self.parse(metric, file_handle)

    def parse(self, module, file_handle):
        f = open(file_handle, 'r', encoding = "ISO-8859-1")
        content = f.read()
        m = re.search(r"METRICS\sCLASS\s*(\w+)\.[^.]*\.(\w+)\n([^\n]+)\n(([^\n#]+\n)+)", content)
        #module = m.group(2)
        columns = m.group(3).split("\t")
        d = m.group(4)
        p = re.search(r"^(PAIR|UNPAIRED)[^\n]*", m.group(4), flags=re.M)
        if p:
            d = p.group(0)
        data = d.strip("\n").split("\t")

        if self.build_ref and module not in self.ref_map:
            metric_map = {}
        else:
            metric_map = self.ref_map[module]

        new_cols = []
        for column in columns:
            if column in metric_map:
                new_cols.append(metric_map[column])
            elif self.build_ref:
                new_col = self.get_mapped_val(module, column)
                metric_map[column] = new_col
                new_cols.append(new_col)
            else:
                log.error("Metric type does not have a mapped code (maybe you need to run with --buildref flag?)")
                raise Exception('Metric type does not have a mapped code')

        data_dictionary = dict(zip(new_cols, data))
        json_table = json.dumps(data_dictionary)
        picard_dict = dict(
            {'db_id': self.db_id, 'qc_program': 'picard', 'qc_metric': module, 'data': json_table})
        self.metrics.append(picard_dict)
