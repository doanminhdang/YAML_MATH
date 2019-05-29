// <output> := <input_[0]> + ... + <input_[end]>
!preparation: //use Python command
{
command_text = "<input_[0]>"
for k in range(1, len(input_)):
  command_text += " + <input_[" + str(k) + "]>"
}
!action:
{
<output> := <command_text>
}
