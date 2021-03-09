<template>
	<view class="content">
		<view class="status">
			<text>{{BLEStatus}}</text>
		</view>
		<view class="btn-container">
			<button class="connect-btn" @click="connect">连接</button>
		</view>
		<view class="input-container">
			<input class="input" type="text" v-model="inputText"></input>
			<button class="send-btn"  @click="send">发送数据</button>
		</view>
		<view class="output-container">
			<view class="title">接收数据</view>
			<view class="output">{{this.content}}</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				title: 'Hello',
				BLEStatus: 'not connected',
				DeviceID: '',
				ServiceUUID: '0000FFE0-0000-1000-8000-00805F9B34FB',
				CharacteristicId: '0000FFE1-0000-1000-8000-00805F9B34FB',
				content: '',
				inputText: ''
			}
		},
		onLoad() {

		},
		methods: {
			connect(){
				uni.openBluetoothAdapter({
					success: (res) => {
						console.log('openBluetoothAdapter success');
						uni.startBluetoothDevicesDiscovery({
							services: ['0000fff0-0000-1000-8000-00805f9b34fb'],
							success: () => {
								console.log('startBluetoothDevicesDiscovery success');
								uni.onBluetoothDeviceFound((res)=>{
									res.devices.forEach(device => { 
										if (device.name == 'HC-04 BLE') {
											this.DeviceID = device.deviceId;
											uni.stopBluetoothDevicesDiscovery({});
											uni.createBLEConnection({
												deviceId: this.DeviceID,
												success: () => {
													console.log('createBLEConnection seccess',this.DeviceID);
													setTimeout(()=>{
														uni.getBLEDeviceServices({
															deviceId:this.DeviceID,  
															success: (res)=> {  
																console.log('getBLEDeviceServices success',res);  
															}
														});
														uni.getBLEDeviceCharacteristics({
															deviceId:this.DeviceID,  
															serviceId:this.ServiceUUID,
															success:(res)=> {  
																console.log('getBLEDeviceCharacteristics success',res); 
															}
														});
														uni.notifyBLECharacteristicValueChange({
															state: true, // 启用 notify 功能  
															deviceId:this.DeviceID,  
															serviceId:this.ServiceUUID,  
															characteristicId:this.CharacteristicId,  
															success:(res)=> {  
																console.log('notifyBLECharacteristicValueChange success');
																this.BLEStatus = 'connection success';
																uni.onBLECharacteristicValueChange((res)=>{
																	console.log(this.ab2hex(res.value));
																	this.content=this.ab2hex(res.value);  
																})
															}
														});
													},1000)
												}
											})
										}
									})
								})
							},
							fail: () => {
								console.log('startBluetoothDevicesDiscovery failed');
							}
						})
					},
					fail: () => {
						console.log('openBluetoothAdapter failed');
					}
				})
			},
			ab2hex(buffer) {
			  const hexArr = Array.prototype.map.call(
			    new Uint8Array(buffer), 
			    function (bit) {
			      return ((bit-48).toString()).slice(-2) 
			    }
			  )
			  return hexArr.join('')
			},
			str2ab(str) {
				let val = ""
				    for (let i = 0; i < str.length; i++) {
				      if (val === '') {
				        val = str.charCodeAt(i).toString(16)
				      } else {
				        val += ',' + str.charCodeAt(i).toString(16)
				      }
				    }
				    return new Uint8Array(val.match(/[\da-f]{2}/gi).map(function (h) {
				      return parseInt(h, 16)
				    })).buffer
			}, 
			send(){
				let buffer=this.str2ab(this.inputText);
				uni.writeBLECharacteristicValue({  
					deviceId:this.DeviceID,  
					serviceId:this.ServiceUUID,  
					characteristicId:this.CharacteristicId,  
					value: buffer,  
					success(res) {  
						console.log('writeBLECharacteristicValue success');
					},  
					fail(res) {
						console.log('writeBLECharacteristicValue failed'); 
					}  
				})  
			}
		}
	}
</script>

<style lang="scss">
	page{
		background: #F4F6F8
	}
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.status {
		margin: 50upx 0upx;
		height: 100upx;
		width: 300upx;
		font-weight: bold;
		font-size: 32upx;
		text-align: center;
		line-height: 100upx;
		/* background-color: #007AFF; */
	}

	.btn-container{
		margin: 50upx 0upx;
		// background-color: #007AFF;
		.connect-btn{
			height: 70upx;
			width: 200upx;
			line-height: 70upx;
		}
	}
	.input-container{
		.input{
			background-color: white;
			height: 100upx;
			width: 600upx;
			margin: 10upx;
		}
		.send-btn{
			margin: 10upx auto;
			height: 70upx;
			line-height: 70upx;
			width: 200upx;
		}
	}
	.output-container{
		height: 100upx;
		width: 600upx;
		margin: 50upx 0;
		.title{
			text-align: center;
		}
		.output{
			height: 80upx;
			width: 500upx;
			margin: 10upx auto;
			background-color: #FFFFFF;
		}
	}
</style>
