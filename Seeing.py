''' 这是森亮号的第一个Sublime的小玩意,用于音频见识转录 '''

import sublime, sublime_plugin
# 导入子进程的玩意
import subprocess
# 系统库
import os,re
import datetime

'''
==TODO==
* 引入倒计时的处理?
* 嗯...下一首再分开一些
* 下一首新见识的时候暂停一些时间在播放...
==Done==
* call单独出来一个函数
==路径==
* 当前放置在路径
: /Users/sen/Documents/AppleScript/音频见识*/
'''

# 集成化的处理调用applescript..
def run_applescript(args):
	base_path = "/Users/sen/Documents/AppleScript/音频见识建造/"
	if type(args)==list:
		script_name = args[0]; # 第一个值
		arg_part = args[1]; # 第二个值
	else:
		script_name = args; # 假设为只有字符串
		arg_part = ""; # 空白
	# 处理,见识替身文件
	scirpt_file = base_path+script_name; # 基础文件名
	if not os.path.isfile(scirpt_file): # 检查替身是否存在
		scirpt_file = scirpt_file+".scpt";
	print("scirpt_file")
	call_command = ["osascript", scirpt_file]; # 呼叫命令
	if arg_part != "":
		call_command.append(arg_part);
	# 基本路径,放置脚本的路径
	return subprocess.check_output(call_command).decode("utf-8");

# 去往航海见识
def go_see(title):
	val = run_applescript(["Chrome 进入航海见识",title]);

# 状态栏提醒
def log(str):
	sublime.status_message(str);

# 获得标题标记
def get_title_flag(content):
	title_re = re.compile(r"\|标题:(.+)\|");
	title=title_re.search(content);
	if title:
		return title.group(1);
	return None; #无效

# 清除标题标记
def clear_title_flag(content):
	#带有吸收换行的正则
	title=re.search(r"(\n*\|标题:.+\|)",content);
	if title:
		return content.replace(title.group(1),"");
	print ("工作异常..."); #不应该这里出现..
	return content

class 当前音频见识(sublime_plugin.TextCommand):
	def run(self, edit):
		# self.window.new_file()
		# 记住当前位置
		pos = self.view.sel()[0].begin();
		val=run_applescript("iTunes 音频见识想法")
		self.view.insert(edit, pos, val)
		s0_region=self.view.find("\$0",0)
		self.view.replace(edit,s0_region,"")
		# 试试移动鼠标好了
		self.view.sel().clear();
		# 去到某个位置去
		self.view.sel().add(s0_region.begin());
		# 后续清理一些别的
		self.view.replace(edit,self.view.find("音频见识",0),"")
		# 这里不允许清楚在标题里的,或许另外的可以直接匹配[音频想法=]
		self.view.replace(edit,self.view.find("(?<!=)音频想法",0),"")
		self.view.replace(edit,self.view.find("	",0),"")
		log("船长,已送出当前音频见识");

class 清理想法(sublime_plugin.TextCommand):
	def run(self,edit):
		self.view.replace(edit,self.view.find("\n+\[\[分类\:想法\]\]",0),"")
        # 更好的做法应该取得位置,减去长度和匹配...
		self.view.replace(edit,self.view.find("非想法",0),"")
		log("船长,已清理分类想法");

class 新音频见识(sublime_plugin.WindowCommand):
	def run(self):
		val=run_applescript("iTunes 下一首");
		syntax = "Packages/Mediawiker-SLboat-Mod/Mediawiki.tmLanguage"
		view = self.window.new_file()
		view.set_syntax_file(syntax)
		view.run_command("当前音频见识")
		log("船长,已在新船长里制造了音频见识");

class 下一首见识(sublime_plugin.WindowCommand):
	def run(self):
		val = run_applescript("iTunes 下一首");
		print(val)
		log("船长,去往下一首了");

class 复制所有(sublime_plugin.TextCommand):
	def run(self, edit):
		title = "";# 默认空白标题
		self.view.run_command("选择所有");
		# 取得所有的内容
		content = self.view.substr(sublime.Region(0, self.view.size()));
		if "[[分类:想法]]" in content: # 是否存在想法
			title = "想法 "; #默认想法
		if get_title_flag(content):
			flag_title=get_title_flag(content); # 获得标题内容
			content = clear_title_flag(content);
			log("船长,发现标题[%s],已送到航海见识..." % flag_title);
			title = title + flag_title + "+"; # 最终标题
		else:
			log("船长,没有标题,直接送到航海见识...");

		# 第一段路-送到剪贴板
		sublime.set_clipboard(content);
		# 第二段路-前往开船...
		go_see(title);
		
class 去往航海见识(sublime_plugin.TextCommand):
	def run(self,edit):
		log("船长,咋去往航海见识咯");
		go_see("")

class 选择所有(sublime_plugin.TextCommand):
	def run(self,edit):
		self.view.sel().clear(); #清理
		self.view.sel().add(sublime.Region(0, self.view.size()))

#后来的发生
class 后来(sublime_plugin.TextCommand):
    def run(self,edit):
        pos = self.view.sel()[0].begin();
        before_content = self.view.substr(sublime.Region(0,pos)); #光标前的内容
        # print("之前的内容",before_content); #调试信息
        datapat = re.compile("\[\[File\:(\d{2})(\d{2})(\d{2})_\d{3}\.MP3\]\]")
        match_date = datapat.search(before_content);
        if match_date:
        	#print (match_date.groups()); #调试用
        	mp3_day = datetime.date(int("20" + match_date.group(1)),int(match_date.group(2)),int(match_date.group(3)));
        	today = datetime.date.today();
        	diffday = today - mp3_day; #差值
        	self.view.insert(edit,pos,"\n:[后来-" + str(diffday.days) + "天后]->")

        else:
        	#todo 移到最后一行
        	self.view.insert(edit,pos,"\n:[后来-若干时间后]->")
        log("当前的位置是" + str(pos));

#暂未使用这里
class 快退(sublime_plugin.WindowCommand):
	def run(self):
		val=run_applescript("iTunes 快退");

class 定时15分钟(sublime_plugin.TextCommand):
	def  run(self,edit):
		subprocess.check_output(["open","timebar://whimsicalifornia.com/start?duration=900"])


class 自动事件(sublime_plugin.EventListener):
	# self是自己,view是试图,prefix就是当前的引导文字,locations则是位置
	def on_query_completions(self, view, word, locations):
		if view.settings().get('syntax').find("Mediawiki")<0:
			return #不是mw,不工作
		if word == "音频见识" or word == "音频想法":
			view.run_command("当前音频见识")
			return
		elif word == "非想法":
			view.run_command("清理想法")
			return
		print("信息:触发了一个"+word)
		return
		# return autocomplete_list
	
	def on_new(self,view): #绑定新窗口自动设置为航海见识
		syntax = "Packages/Mediawiker-SLboat-Mod/Mediawiki.tmLanguage"
		view.set_syntax_file(syntax)