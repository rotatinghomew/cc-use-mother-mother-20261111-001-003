基层转诊挂号可恢复RPA
基层转诊员通过可回放页面夹具执行挂号录入，遇到验证码、页面漂移或最终提交必须停在人工确认点并可从检查点恢复。

测试：python3 -m unittest discover -s tests/appointment_robot -p 'test_*.py'
构建：python3 -m compileall -q referral_robot tests/appointment_robot
验收：python3 -m referral_robot.console.runbook --fixture fixtures/demo.json --database /tmp/appointment_robot-acceptance.sqlite3
