# guide to use dashmnb with trezor
- - - -
## 1. read FAQ, user mannual, cryptography and web wallet
* [TREZOR Frequently Asked Questions — TREZOR Frequently Asked Questions 1.0 documentation](https://doc.satoshilabs.com/trezor-faq/index.html) 
* [TREZOR User Manual — TREZOR User Manual 1.0 documentation](https://doc.satoshilabs.com/trezor-user/index.html) 
* [Cryptography — TREZOR Developer’s guide 1.0 documentation](https://doc.satoshilabs.com/trezor-tech/cryptography.html) 
* [TREZOR Wallet — TREZOR Apps 1.0 documentation](https://doc.satoshilabs.com/trezor-apps/trezorwallet.html)

## 2. what is dashmnb
![](https://raw.githubusercontent.com/chaeplin/dashmnb/master/others/pics/dashmnb2.png)

> dashmnb is a python 3 script to broadcast the MN start message signed by hw wallet  to network via dashcore.  dashmnb has command options,  
> 1) starting mn(s)  
> 2) checking mn(s) status  
> 3) checking blance of mn(s)  
> 4) voting a proposal  
> 5) making a tx(to send reward(s) received)  
> 6) whale mode(automaticaly yes to all question except asked by hw wallet)  

## 3. which OS supported(tested)
		- system has python version > 3.5.1
		- Ubuntu 16.04
		- Ubuntu 14.04
		- Debian 8.7.1
		- Windows 10
		- Windows 7
		- Mac OSX

## 4. why installation and configuration of dashmnb is so “hacky  / geeky” ?
> dashmnb uses python Virtualenv.  Prerequisites is a step to prepare python Virtualenv.  
`What is Virtualenv?`
`Virtualenv is a tool to create isolated Python environments, it's perhaps the `
`easiest way to configure a custom Python environment. `

`Virtualenv allows you to add and modify Python modules without access to the`
`global installation.    `  

> installation of dashmnb is simple. clone githup repo and run install script.  

> configuration of dashmnb needs servral steps  
> 1) select sample config.py - with your own dashcore or without  
> 2) move fund(s) to hw wallt(can be done before installation and configuration  
> 3) edit config.py  
> 4) edit mastenode.conf  

## 5. links for installtion
* [Ubuntu 16.04](https://github.com/chaeplin/dashmnb/tree/master/others/pics/ubuntu-16.04)
* [Ubuntu 14.04](https://github.com/chaeplin/dashmnb/tree/master/others/pics/ubuntu-14.04)
* [Debian 8.1](https://github.com/chaeplin/dashmnb/tree/master/others/pics/debian-8.7.1)
* [Windows 10 / 7](https://github.com/chaeplin/dashmnb/tree/master/others/pics/windows10)
* [Max OSX](https://github.com/chaeplin/dashmnb#1b-install-prerequisites-mac-os)

## 6. links for configuration
* [configuration](https://github.com/chaeplin/dashmnb#configuration)
