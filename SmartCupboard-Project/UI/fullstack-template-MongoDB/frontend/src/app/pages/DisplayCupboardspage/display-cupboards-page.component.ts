import { Component, OnInit, ViewChild } from '@angular/core';
import { SocketsService } from 'src/app/global/services';
import { ElementRef } from '@angular/core';
import { AfterViewInit } from '@angular/core';


@Component({
  selector: 'ami-fullstack-display-cupboards-page',
  templateUrl: './display-cupboards-page.component.html',
  styleUrls: ['./display-cupboards-page.component.scss']
})


export class DisplayCupboardsPageComponent implements OnInit { // , AfterViewInit

  // @ViewChild('innerColor') innerColor!: ElementRef;
  @ViewChild("innerRightColor", { static: true }) innerRightColor: ElementRef;
  @ViewChild("innerLeftColor", { static: true }) innerLeftColor: ElementRef;

  data : any;
  cupId : any;
  color : any;


  constructor(private socketService: SocketsService) { }

  ngOnInit() {
  
    this.cupId = 2; // initialize cupId to 2
    this.color = 'transparent'; // initialize color to red

    this.innerLeftColor.nativeElement.style.backgroundColor = this.color;
  

  }

  ngAfterViewInit(){
    
    this.innerLeftColor.nativeElement.style.backgroundColor = this.color;

    
    
    this.socketService.syncMessages("lightVirtualCupsDoors").subscribe(msg => {
      this.data = msg["message"] ; // {cupId: 3, color: 'green'}
      
      console.log('data  : ',this.data); // debug

      this.cupId = this.data["cupId"];
      this.color = this.data["color"];

      console.log('cupId  : ',this.cupId); // debug
      console.log('color  : ',this.color); // debug

      
      if (this.cupId == 2) {
        this.innerLeftColor.nativeElement.style.backgroundColor = this.color;
        this.innerLeftColor.nativeElement.style.visibility = 'visible';
        this.innerRightColor.nativeElement.style.visibility = 'hidden';
      }
      else if (this.cupId == 3) {
        this.innerRightColor.nativeElement.style.backgroundColor = this.color;
        this.innerRightColor.nativeElement.style.visibility = 'visible';
        this.innerLeftColor.nativeElement.style.visibility = 'hidden';
      }
      else {
        console.log('error : cupId is not 2 or 3');
        this.innerRightColor.nativeElement.style.backgroundColor = this.color;
        this.innerLeftColor.nativeElement.style.backgroundColor = this.color;
      }

    })
  }

}
