import { getLocaleDayNames } from '@angular/common';
import { Component, OnInit,Input,Output,EventEmitter } from '@angular/core';

@Component({
  selector: 'ami-fullstack-bottom-bar',
  templateUrl: './bottom-bar.component.html',
  styleUrls: ['./bottom-bar.component.scss']
})


export class BottomBarComponent implements OnInit {

  currentNumPage: number = 1 ; // initialize 
  totalNumPages: any ; //number = 4 ; // That is the result after the sorting (top bar button selection)

  @Output() newPressedPageEvent = new EventEmitter<any>();
  
  public sendInfoEvent(value: any) {
    this.newPressedPageEvent.emit(value); // send info to parent component
  }

  @Input() public set totalPages(value: any) {
    this.totalNumPages = value ; 
  }
  constructor() { }

  ngOnInit() {
  }

  goToPreviousPage(pageNum:number){
   
    if (pageNum > 1 && pageNum <= this.totalNumPages){
      this.currentNumPage --;
    }

    else{
      this.currentNumPage = 1 ;
    }
    
    this.sendInfoEvent(this.currentNumPage) ;   // send to home component parent the current page info
  }
  
  goToNextPage(pageNum:number){

    if (pageNum >= 1 && pageNum < this.totalNumPages){
      this.currentNumPage ++;
    }
    
    else{
      this.currentNumPage = this.totalNumPages ;
    }
    
    this.sendInfoEvent(this.currentNumPage) ; // send to home component parent the current page info  
    
  }
}
