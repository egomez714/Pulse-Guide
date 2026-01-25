import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';
// imports file for backend url
import '../config.dart';

class SocketService{
  
  // creates websocket named channel
  WebSocketChannel? _channel;

  // checks if connection is made
  Function(bool isConnected)? onConnectionChange;
  
  // connects to websocket
  void connect(){
    try{
      
      print("Connecting to backend at ${Config.backendUrl}...");
      
      // connects websocket to our backend
      _channel = WebSocketChannel.connect(Uri.parse(Config.backendUrl));

      onConnectionChange?.call(true);
      print("connnected");
    
    } catch(e){
      print("Error, could not connect to backend: $e");
    }
  }
  
  void sendFrame(List<int> imageBytes){
    
    if(_channel != null){
      // sends image frame to backend
      _channel!.sink.add(imageBytes);
    
    }
  
  }

  // listens for backend
  Stream get messages => _channel!.stream;


  void disconnect(){
    _channel?.sink.close();
    onConnectionChange?.call(false);
  }

}