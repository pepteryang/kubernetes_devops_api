#-*-coding:utf-8-*-
# @Author : yangzhiqun
# @Email : zhiqun.yang@bqrzzl.com
# @Time : 2018/10/08 14:13
# @Site :
# @File : es_api.py
# @Software : PyCharm

# https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch

from elasticsearch import Elasticsearch
from elasticsearch import helpers


class ElasticSearchQuery:
    # make sure ES is up and running
    def __init__(self, es_cluster_host, es_cluster_port, query_es_index, query_str_must_not, query_str_must, date):
        self.es_cluster_host = es_cluster_host
        self.es_cluster_port = es_cluster_port
        self.query_es_index = query_es_index
        self.query_str_must_not = query_str_must_not
        self.query_str_must = query_str_must
        self.date = date
        # 实例化ElasticSearch类，并设置超时间为180秒，默认是10秒的，如果数据量很大，时间设置更长一些
        self.es = Elasticsearch(
            [self.es_cluster_host],
            http_auth=('', ''),
            scheme="http",
            port=self.es_cluster_port,
            timeout=180)

    def _query_data(self):
        gte = "now-" + str(self.date)
        body = {"query": {
            "bool": {
                "should": {
                    # 查询条件，相当于OR条件
                },
                "must_not":{
                    # 必须匹配的条件，这里的条件都会被反义
                    "query_string": {
                        "query": self.query_str_must_not,
                        }
                },
                "must": {
                    # 必须要有的
                    "query_string": {
                        "query": self.query_str_must,
                        }
                    },
                    "filter": {
                        # 过滤范围
                        "range": {
                          "@timestamp": {
                            "gte": gte,
                            "lt": "now",
                            "format": "epoch_millis"
                          }
                        }
                    }
                }
            }
        }
        return body

    def _get_data(self):
        """
        :param index_name: 索引名称
        :param keywords: 关键字词，数组
        :param param: 需要数据条件，例如_source
        :param date: 过去时间范围,字符串格式，例如过去30分钟内数据，"30m"
        :return: all_data 返回查询到的所有数据（已经过param过滤）
        """
        all_data = []
        # 遍历所有的查询条件
        query = self._query_data()
        res = self.es.search(index=self.query_es_index, body=query)
        for i in range(0, len(res['hits']['hits'])):
            # 获取指定的内容
            response = res['hits']['hits'][i]['_source']['message']
            # 添加所有数据到数据集中
            all_data.append(response)
        # 返回所有数据内容
        return all_data


class DeleteIndex(object):
    def __init__(self, es_cluster_host, es_cluster_port):
        self.es_cluster_host = es_cluster_host
        self.es_cluster_port = es_cluster_port
        self.es = Elasticsearch([self.es_cluster_host], http_auth=('', ''), scheme="http", port=self.es_cluster_port,)

    def delete_index(self, delete_index=None):
        self.es.indices.delete(delete_index, ignore=[400, 404])
