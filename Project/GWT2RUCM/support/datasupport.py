import sqlite3
from data.datatype import GWT, TaggedGWT, Sentence, TaggedSentence, Association, Scenario


def connect_db():
    
    """
    Connects to the specific database.
    在此之前你需要使用init.sql文件构建数据库
    当前使用内部sqlite数据库
    """
    rv = sqlite3.connect('db')
    rv.row_factory = sqlite3.Row
    rv.cursor().executescript(r'../init.sql')#执行sql脚本init
    return rv


'''
context backgroundDao::getContentList
context backgroundDao::insert
context backgroundDao::update

context GWTDao::getGWTListById(id int):GWT or False
    pre:if Tagged then flowType != None
        异常检测
    post: return = if 成功得到 then GWT or TaggedGWT else False
context GWTDao::getId_Scenario_List():(GWT.id:int,GWT.Scenario:String)List
    pre:异常检测
    post: return = result
context GWTDao::insert_gwt(data:GWT):
    pre: 异常检测
         该GWT的Scenario是独一无二的
         if Tagged then flowType != None
         Scenario必须是String类型
         Givens,Whens,Thens,Features都必须是列表类型
         插入的GWT均为未打标签的GWT，即只有Content:String和Sequence:Int
         Feature一经导入不再改变
    post: 将该GWT导入，并自动生成id号
context GWTDao::insert_Tagged_gwt(data:GWT):Boolean
    pre: 异常检测
         该GWT的Scenario已经存入数据库中，且传入的GWT的gwt_id需要在数据库中，不然不进行更新
         该GWT为TaggedGWT
         TaggedSentence两边都需加上对方的关联标签，虽然这样会比较浪费空间，但是便于查询，以后可以进行修改
         Feature一经导入不再改变
    post: return = result
'''


class GWTdao(object):
    def __init__(self):
        self.__connection = connect_db()

    def __del__(self):
        self.__connection.close()

    def get_gwt_list_by_id(self, gwtIdList):
        '''
        #patrick
        if not isinstance(gwt_id, int):
            return False
        '''
        gwtList=[]
        for gwt_id in gwtIdList:
            gwt = TaggedGWT()
            tmps = self.__connection.execute('select * from GWT_tb where id=' + str(gwt_id)).fetchall()
            gwt.gwt_id = tmps[0][0]
            gwt.Scenario = tmps[0][1]
            gwt.useCaseName = tmps[0][2]
            gwt.flowType = tmps[0][3]
            gwt.Features = []
            gwt.Givens = []
            gwt.Whens = []
            gwt.Thens = []
            tmps = self.__connection.execute(
                'select Sentence.id, Sentence.Stype, Sentence.secondType, Sentence.content, Sentence.sequence, gwtSentence.position_in_gwt  from Sentence inner join gwtSentence on gwtSentence.sentence_id=Sentence.id where gwt_id=' + str(
                    gwt_id))
            for tmp in tmps:
                stmp = TaggedSentence()
                stmp.sentence_id = tmp[0]
                stmp.type = tmp[1]
                stmp.secondType = tmp[2]
                stmp.content = tmp[3]
                stmp.sequence = tmp[4]
                if gwt.flowType is not None:
                    stmp.associations = []
                    ts = self.__connection.execute(
                        'select SentenceSentence.s2, SentenceSentence.connectType from SentenceSentence where s1=' + str(
                            stmp.sentence_id))
                    for t in ts:
                        connect = Association()
                        connect.sentenceId = t[0]
                        connect.connect_type = t[1]
                        tt = self.__connection.execute(
                            'select gwt_id from gwtSentence where sentence_id=' + str(connect.sentenceId))
                        # 暂时不考虑优化问题，相同句子同样存储在不同sentence中
                        connect.gwtId = tt[0][0]
                        stmp.associations.append(connect)
                if tmp[5] is 'feature':
                    gwt.Features.append(stmp)
                elif tmp[5] is 'given':
                    gwt.Givens.append(stmp)
                elif tmp[5] is 'when':
                    gwt.Whens.append(stmp)
                elif tmp[5] is 'then':
                    gwt.Thens.append(stmp)
                else:
                    return False
                gwtList.append(gwt)
        return gwtList

    def get_id_scenario_list(self):
        '''
        获取的内容用于网页展示GWT概况供用户选择
        '''
        return self.__connection.execute('select id,scenario from GWT_tb').fetchall()

    def insert_gwt(self, gwt):
        self.__connection.execute("insert into GWT_tb(scenario) values ('%s')" % (str(gwt.Scenario)))
        self.__connection.commit()
        tmp0 = self.__connection.execute("select last_insert_rowid()").fetchall()
        tmp0 = tmp0[0][0]
        for t in gwt.Features:
            self.__connection.execute("insert into Sentence(content) values ('%s')" % t.content)
            self.__connection.commit()
            tmp1 = self.__connection.execute("select last_insert_rowid()").fetchall()
            self.__connection.execute(
                "insert into gwtSentence values ('%s','%s','%s')" % (str(tmp0), str(tmp1[0][0]), 'feature'))
        for t in gwt.Givens:
            self.__connection.execute("insert into Sentence(content) values ('%s')" % t.content)
            self.__connection.commit()
            tmp1 = self.__connection.execute("select last_insert_rowid()").fetchall()
            self.__connection.execute(
                "insert into gwtSentence values ('%s','%s','%s')" % (str(tmp0), str(tmp1[0][0]), 'given'))
        for t in gwt.Thens:
            self.__connection.execute("insert into Sentence(content) values ('%s')" % t.content)
            self.__connection.commit()
            tmp1 = self.__connection.execute("select last_insert_rowid()").fetchall()
            self.__connection.execute(
                "insert into gwtSentence values ('%s','%s','%s')" % (str(tmp0), str(tmp1[0][0]), 'then'))
        for t in gwt.Whens:
            self.__connection.execute(
                "insert into Sentence(content,sequence) values ('%s','%s')" % (t.content, str(t.sequence)))
            self.__connection.commit()
            tmp1 = self.__connection.execute("select last_insert_rowid()").fetchall()
            self.__connection.execute(
                "insert into gwtSentence values ('%s','%s','%s')" % (str(tmp0), str(tmp1[0][0]), 'when'))
        self.__connection.commit()

    def insert_Tagged_gwt(self, gwt):
        sql = "update GWT_tb set useCaseName = ?, flowType = ? where id = ?"
        self.__connection.execute(sql, [str(gwt.useCaseName), str(gwt.flowType), str(gwt.gwt_id)])
        sql_change_type = "update Sentence set Stype=?, secondType=? where id = ?"
        sql_insert_association = "insert into SentenceSentence values (?,?,?)"
        for t in gwt.Givens:
            self.__connection.execute(sql_change_type, [t.type, t.secondType])
            for x in t.associations:
                self.__connection.execute(sql_insert_association,
                                          [str(t.sentence_id), str(x.sentenceId), x.connect_type])
        for t in gwt.Thens:
            self.__connection.execute(sql_change_type, [t.type, t.secondType])
            for x in t.associations:
                self.__connection.execute(sql_insert_association,
                                          [str(t.sentence_id), str(x.sentenceId), x.connect_type])
        for t in gwt.Whens:
            self.__connection.execute(sql_change_type, [t.type, t.secondType])
            for x in t.associations:
                self.__connection.execute(sql_insert_association,
                                          [str(t.sentence_id), str(x.sentenceId), x.connect_type])
