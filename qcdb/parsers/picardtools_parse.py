from qcdb.parsers.parse import BaseParser
import json, logging, os, glob2, re

log = logging.getLogger(__name__)
dirname = os.path.dirname('__file__')

class picardtoolsParser(BaseParser):
    
    def __init__(self, file_handle):
        log.info("Initializing picardtoolsParser...")
        BaseParser.__init__(self,file_handle,'picard')       
        file_table_dict = {'insertsizemetrics': 'insertsize_metrics_picard',
            'alignmentmetrics': 'alignment_summary_metrics_picard', 
            'gcbiasmetrics': 'summary_gcbias_metrics_picard'}
        self.parse(file_table_dict, os.path.dirname(file_handle))

    def parse(self, ft_dict, directory):
        for module, name in ft_dict.items():
            log.info("Parsing {} into {}...".format(name, module))
            files = glob2.glob(os.path.join(directory,
'{}_{}_*{}.txt'.format(self.sample_name,self.experiment,name)))

            for file in files:
                f = open(file, 'r', encoding = "ISO-8859-1")           
                content = f.read()
                m = re.search(r"METRICS\sCLASS\s*(\w+)\.[^.]*\.(\w+)\n([^\n]+)\n(([^\n#]+\n)+)", content)
                #module = m.group(2)
                header = m.group(3).split("\t")
                d = m.group(4)
                p = re.search(r"^(PAIR|UNPAIRED)[^\n]*", m.group(4), flags=re.M)
                if p:
                    d = p.group(0)
                data = d.strip("\n").split("\t")
                data_dictionary = dict(zip(header, data))
                json_table = json.dumps(data_dictionary)
                picard_dict = dict(
                    {'sample_id': self.sample_id, 'qc_program': 'picard', 'qc_metric': module, 'data': json_table})
                self.metrics.append(picard_dict)
