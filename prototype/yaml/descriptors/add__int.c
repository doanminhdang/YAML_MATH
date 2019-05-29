!preprocess:
{|
# Python 3 commands
command_text = "<input_[0]>"
for k in range(1, len(input_)):
  command_text += " + <input_[" + str(k) + "]>"
|}
!template:
{|
<output> := <command_text>
|}
