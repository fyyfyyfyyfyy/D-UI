
# Eilik 接口

## 底层

执行动作 S：`(0x02,0x03, action_id)`
无返回

读取状态 S：`(0x01,0x01)`
返回值：(head_status, front_status, back_status)
返回值 >= 2 则按下
