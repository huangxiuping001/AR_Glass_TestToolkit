import os

from bs4 import BeautifulSoup

from utils.filetools import fileUtils

from html5print import HTMLBeautifier

child_content = '''
    <div style="width: 900px; margin: 0 auto;margin-top: 50px;">
        <h2>html_report_sub_title_012345</h2>

        html_report_child_content_012345

        <div style="margin-top: 20px;">
            html_report_child_desc_012345
        </div>
    </div>
    '''

class HtmlUtils(object):
    def __init__(self):
        self.base = BeautifulSoup(open('base_html.html'), 'lxml').prettify()

    def createHtmlReport(self, title = '', html_bean_list = [], file_name = ''):

        self.base = self.base.replace('html_report_title_012345', title)

        content = ''

        for item in html_bean_list:
            if not item:
                continue

            temp = child_content
            temp = temp.replace('html_report_sub_title_012345', item.sub_title)

            graphy = ''
            for file in item.html_files:
                if not file.endswith('.html'):
                    continue

                print(str(BeautifulSoup(open(file), 'lxml').body.div))

                if graphy:
                    t1 = str(BeautifulSoup(open(file), 'lxml').body.div)
                    graphy += t1.replace('width', 'margin-top: 30px;width')
                    graphy += '\n'
                else:
                    graphy += str(BeautifulSoup(open(file), 'lxml').body.div)
                    graphy += '\n'
                graphy += str(BeautifulSoup(open(file), 'lxml').body.script)
                graphy += '\n'

            temp = temp.replace('html_report_child_content_012345', graphy)

            text_area = ''
            for desc in item.desc_list:
                text_area += '<h4>%s</h4>\n'%(desc)

            temp = temp.replace('html_report_child_desc_012345', text_area)
            temp += '\n'

            content += temp

        self.base = self.base.replace('html_report_content_012345', content)

        if os.path.exists(file_name):
            fileUtils.clean_file(file_name)

        # self.base = BeautifulSoup(self.base, features='lxml').prettify()

        fileUtils.write_file(file_name, HTMLBeautifier.beautify(self.base, 4))

class HtmlBean(object):

    def __init__(self, html_files=[], sub_title='这是标题', desc_list = []):
        self.html_files = html_files
        self.sub_title = sub_title
        self.desc_list = desc_list

if __name__ == '__main__':
    hu = HtmlUtils()

    hu.createHtmlReport('测试自动生成测试报告',
                        [HtmlBean(['E:\python_home\\translator__android__test_toolkit\property\OfflineEnginePerformance\\html_file\\test.html'],
                                  '测试子标题1',
                                  ['1、测试结论文本', '2、测试结论文本']),
                         HtmlBean(['E:\python_home\\translator__android__test_toolkit\property\OfflineEnginePerformance\\html_file\\test_compile.html',
                                   'E:\python_home\\translator__android__test_toolkit\property\OfflineEnginePerformance\\html_file\\test_compile_esr.html'],
                                  '测试子标题2',
                                  ['1、测试结论文本', '2、测试结论文本'])
                         ],
                        'auto_html.html')