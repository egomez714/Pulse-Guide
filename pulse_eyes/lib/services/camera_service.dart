// timer
import 'dart:async';
// handle raw image bytes
import 'dart:typed_data';
// to use hardware 
import 'package:camera/camera.dart';
// logs
import 'package:flutter/foundation.dart';

class CameraService{
  
  CameraController? _controller;
  bool _isStreaming = false;
  
  Function()? onCameraInitialized;

  Future<void> initialize() async{
    try{

      final cameras = await availableCameras();
      
      if(cameras.isEmpty) return;

      _controller = CameraController(
        cameras.first,
        ResolutionPreset.medium,
        enableAudio:false,
        imageFormatGroup: ImageFormatGroup.jpeg,
      );
      
      await _controller!.initialize();
      onCameraInitialized?.call();

    } catch(e){
      if (kDebugMode) print("Camera not initialized: $e");
    }
  }

  void startStreaming(Function(Uint8List) onFrameCaptured){
    if (_controller == null || _isStreaming) return;
    _isStreaming = true;

    // creates endless loop, takes picture 2 timens a second
    Timer.periodic(const Duration(milliseconds: 500), (timer) async {
      if (!_isStreaming || _controller == null) {
        timer.cancel();
        return;
      }
      try {
        final XFile file = await _controller!.takePicture();
        final bytes = await file.readAsBytes();
        onFrameCaptured(bytes);
      }catch (e){
        print("Snapshot error: $e");
      }
    });
  }


}