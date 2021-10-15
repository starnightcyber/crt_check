# crt_check
批量检测证书是否过期

## 项目文件说明

```
.
├── crt_check.py → 检测脚本
├── crt_info.csv → 输出检测结果文件
├── requirements.txt → 安装依赖包
└── target_file.txt → 需要检查的目标地址，以 host:port 形式提供
```

## 使用
### 安装依赖
```
cd ./crt_check
pip3 install -r requirements.txt -i https://pypi.douban.com/simple
```

### 运行
```
# python3 crt_check.py

[1, 'www.baidu.com', '443', 'https://www.baidu.com:443', '2021-07-01 01:16:03', '2022-08-02 01:16:03', False, 'baidu.com', 'GlobalSign Organization Validation CA - SHA256 - G2', '-']
```


## 其它
大家可以根据自己的需要进行修改，比如增加域名到期提醒，如：邮件、短信或企业微信等告警。
