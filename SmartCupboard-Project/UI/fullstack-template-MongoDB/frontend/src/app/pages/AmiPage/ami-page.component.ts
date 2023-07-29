import { Component, OnInit } from '@angular/core';
import { SocketsService } from 'src/app/global/services';

@Component({
  selector: 'ami-fullstack-ami-page',
  templateUrl: './ami-page.component.html',
  styleUrls: ['./ami-page.component.scss']
})
export class AmiPageComponent implements OnInit {

  PhotoDisplay_filePath: any;
  pageNum: any;
  constructor(private socketService: SocketsService) { }

  ngOnInit() {


    this.pageNum = 0; // initialize pageNum to 0
    this.PhotoDisplay_filePath = "assets/images_marios/Ami_Chef_IntroImage.png"; // initialize the filename to the first image

    this.socketService.syncMessages("amiPages").subscribe(msg => {
      this.pageNum = msg["message"]["pageNum"];

      console.log('PageNum : ',this.pageNum);
      this.changeFileName(); // call the function to change the filename according to the pageNum value

    })

    this.changeFileName(); // call the function to change the filename according to the pageNum value
  }

  // create a function to change the filename variable according the pageNum value
  public changeFileName() {
    if (this.pageNum == 0) {
      this.PhotoDisplay_filePath = "assets/images_marios/Ami_Chef_IntroImage.png"; // initialize the filename to the first image
    }

    else if (this.pageNum == 1) {
      this.PhotoDisplay_filePath = "assets/images_marios/step1_intro.png";
    }
    else if (this.pageNum == 2) {
      this.PhotoDisplay_filePath = "assets/images_marios/step2_rice.png";
    }
    else if (this.pageNum == 3) {
      this.PhotoDisplay_filePath = "assets/images_marios/step3_sugar.png";
    }
    else if (this.pageNum == 4) {
      this.PhotoDisplay_filePath = "assets/images_marios/step_4.png";
    }
    else if (this.pageNum == 5) {
      this.PhotoDisplay_filePath = "assets/images_marios/step_5.png";
    }
    else if (this.pageNum == 6) {
      this.PhotoDisplay_filePath = "assets/images_marios/step_6.png";
    }
    else if (this.pageNum == 7) {
      this.PhotoDisplay_filePath = "assets/images_marios/step_7.png";
    }
    else if (this.pageNum == 8) {
      this.PhotoDisplay_filePath = "assets/images_marios/step_8.png";
    }
    else if (this.pageNum == 9) {
      this.PhotoDisplay_filePath = "assets/images_marios/step_9.png";
    }
    else if (this.pageNum == 10) {
      this.PhotoDisplay_filePath = "assets/images_marios/storingKItchen.png";
    }
    else {
      console.log("error in changeFileName function");
    }

  }
}