''' 这是森亮号的第一个小玩意 '''

import sublime, sublime_plugin
# 导入子进程的玩意
import subprocess

class 当前音频见识(sublime_plugin.TextCommand):
	def run(self, edit):
		# self.window.new_file()
		# 记住当前位置
		pos = self.view.sel()[0].begin();
		script_path="/Users/sen/Documents/AppleScript/音频见识.scpt"
		val=subprocess.check_output(["osascript", script_path])
		val=val.decode("utf-8")
		self.view.insert(edit, pos, val)
		s0_region=self.view.find("\$0",0)
		self.view.replace(edit,s0_region,"")
		# 试试移动鼠标好了
		self.view.sel().clear();
		# 去到某个位置去
		self.view.sel().add(s0_region.begin());
		# 后续清理一些别的
		self.view.replace(edit,self.view.find("音频见识",0),"")
		self.view.replace(edit,self.view.find("	",0),"")

class 清理想法(sublime_plugin.TextCommand):
	def run(self,edit):
		self.view.replace(edit,self.view.find("\[\[分类\:想法\]\]",0),"")
		self.view.replace(edit,self.view.find("非想法",0),"")

class 新音频见识(sublime_plugin.WindowCommand):
	def run(self):
		script_path="/Users/sen/Documents/AppleScript/iTunes 下一首.scpt"
		val=subprocess.check_output(["osascript", script_path])
		syntax = "Packages/Mediawiker-SLboat-Mod/Mediawiki.tmLanguage"
		view = self.window.new_file()
		view.set_syntax_file(syntax)
		view.run_command("当前音频见识")


class 自动事件(sublime_plugin.EventListener):
	# self是自己,view是试图,prefix就是当前的引导文字,locations则是位置
	def on_query_completions(self, view, word, locations):
		if view.settings().get('syntax').find("Mediawiki")<0:
			return #不是mw,不工作
		if word == "音频见识":
			view.run_command("当前音频见识")
			return
		elif word == "非想法":
			view.run_command("清理想法")
			return
		print("触发了一个"+word)
		# return autocomplete_list

	def on_new(self,view): #绑定新窗口自动设置为航海见识
		syntax = "Packages/Mediawiker-SLboat-Mod/Mediawiki.tmLanguage"
		view.set_syntax_file(syntax)