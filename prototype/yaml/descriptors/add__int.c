!preprocess:
{|
# Python 3 commands
command_text = "<input_[0]>"
for k in range(1, len(input_)):
  command_text += " + <input_[" + str(k) + "]>"
|}
!code:
{|
<output> := <command_text>
|}
!postprocess:
{|
code = <code>
|}
