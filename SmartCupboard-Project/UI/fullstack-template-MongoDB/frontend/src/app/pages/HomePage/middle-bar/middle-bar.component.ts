import { Component, OnInit,Input } from '@angular/core';

@Component({
  selector: 'ami-fullstack-middle-bar',
  templateUrl: './middle-bar.component.html',
  styleUrls: ['./middle-bar.component.scss']
})



export class MiddleBarComponent implements OnInit {

  dataReceivedToMiddleBar : any ; 
  pageCurrent : any ;
  dataToShowToCol1 : any ;
  dataToShowToCol2 : any ;
  startIdxCol1 : any ;
  startIdxCol2 : any ;
  endIdxCol1 : any ;
  endIdxCol2 : any ;


  @Input() public set pageNum(value: any) {
    this.pageCurrent = value ;
    console.log('I am in middleBar ... pageNum : ' , this.pageCurrent); // debug
  }

  @Input() public set dataToShow(value: any) {
    
    this.dataReceivedToMiddleBar = value ; 
    console.log("dataReceivedToMiddleBar");
    console.log(this.dataReceivedToMiddleBar);
  }

  public handleData(){
    console.log('Data printed in middle bar ',this.dataReceivedToMiddleBar); // debug
    console.log('I am in middleBar handleData function ... pageNum : ' , this.pageCurrent); // debug 


    this.startIdxCol1 = (this.pageCurrent - 1 ) * 6 ; 
    this.endIdxCol1 = this.startIdxCol1 + 2 ;
    this.dataToShowToCol1 = this.dataReceivedToMiddleBar.slice(this.startIdxCol1, this.endIdxCol1+1) ; 
    console.log('Data to pass to col1...' , this.dataToShowToCol1); // debug


    this.startIdxCol2 = this.endIdxCol1 + 1 ; 
    this.endIdxCol2 = this.startIdxCol2 + 2 ; 
    this.dataToShowToCol2 = this.dataReceivedToMiddleBar.slice(this.startIdxCol2, this.endIdxCol2+1) ; 
    console.log('Data to pass to col2...' , this.dataToShowToCol2); // debug
    
  }

  constructor() { }

  ngOnInit() {
  }

  ngOnChanges(){
    this.handleData();
  }
}
