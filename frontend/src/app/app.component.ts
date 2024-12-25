import '@angular/compiler'
import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common'; // ייבוא ה-CommonModule
import { HttpClientModule } from '@angular/common/http'; // ייבוא המודול
import { DataService } from './services/data.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports:[
    RouterOutlet,
    FormsModule,
    CommonModule,
    HttpClientModule,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {

  posts: any[] = [];

  constructor(private dataService: DataService) {}

  resit: number = 0;
  money: number | null = null;
  home: string = '';
  day: string = '';
  user: string = '';
  why: string = '';
  dataFrom: any[] = [];
  homeId: string = '';
  dataError = '';
  index: number = 0;
  id: number = 0;
  responseMessage: string = '';
  tableData: { resit: number; money: number | null; home: string; day: string; user: string; why: string }[] = [];


  deleteResitAndRow(event: Event, resit: number, index: number): void {
    event.preventDefault();


    console.log('Sending DELETE request to Flask for resit:', resit);


    // בקשת HTTP למחיקת הנתון
    this.dataService.deletePost('resit', resit).subscribe({
      next: (response: any) => {
        console.log('Response from backend:', response);

        // טיפול בתגובה מהשרת
        if (response.message === 'resit not found') {
          alert('הרשומה לא נמצאה');
        } else {
          alert('הרשומה נמחקה בהצלחה');
          // מחיקת השורה מהגרף לאחר שהמחיקה בשרת הצליחה
          this.deleteRow(index);
        }

        // עדכון הודעת שגיאה אם יש
        this.dataError = response.message;
      },
      error: (error:  any) => {
        console.error('Error during DELETE request:', error);
        alert('שגיאה במחיקה, נסה שוב');
      },
    });
  }

  // מחיקת שורה מהגרף
  deleteRow(index: number): void {
    console.log('Deleting row at index:', index);
    this.dataFrom.splice(index, 1);
  }


  // ערך נבחר
  selectedValue: string = '';
  case: any[] = [];

  // פונקציה לבחירת שורה
  selectRow(row: any): void {
    const isAlreadySelected = this.case.includes(row.resit); // בדיקה אם הערך כבר במערך

    if (isAlreadySelected) {
      // לחיצה שנייה - הסר את הערך מהמבחר
      this.case = this.case.filter((resit) => resit !== row.resit); // הסר את הערך
      this.selectedValue = '' ; // נקה את הערך הנבחר
      console.log('קבלה הוסרה:', row.resit); // הצג הודעה בקונסול
      this.case.splice(row.resit);
      this.selectedValue = row.resit; // עדכן את הערך הנבחר
      console.log('נמחקה:', row.resit); // הצג הודעה בקונסול
    } else {
      // לחיצה ראשונה - הוסף את הערך למבחר
      if (this.case.length < 8) {
        this.case.push(row.resit); // הוסף את הערך
        this.selectedValue = row.resit; // עדכן את הערך הנבחר
        console.log('קבלה נבחרה:', row.resit); // הצג הודעה בקונסול
      } else {
        alert('ניתן לבחור עד 8 שורות בלבד!');
      }
    }
  }





  postData(event: Event): void{
    event.preventDefault();

    const data = { resit: this.resit, money: this.money, home: this.home, day: this.day, why: this.why };
    console.log('Data sent to backend', data)
    this.dataService.sendData('control', data).subscribe({
      next: (response: any) => {
        console.log('Response from backend:', response); // בדוק את התגובה
        this.responseMessage = response.message; // שומר את תשובת השרת
      },
      error: (error: any) => {
        console.error('Error:', error);
        this.responseMessage = 'Error occurred while sending data.';
      }
    });
    this.resit = 0;
    this.money = null;
    this.home = '';
    this.day = '';
    this.user = '';
    this.why = '';

  }


  getDataUser(event: Event): void{
    event.preventDefault();
    console.log('GET to Flask')
    this.dataService.getData('control').subscribe({
      next: (response: any) => {
        console.log('Response from backend:', response); // בדוק את התגובה
        this.dataFrom = response;

      },
      error: (error: any) => {
        console.error('Error:', error);

      }
    })
  }

  bataHome(event: Event, homeId: string): void{
    event.preventDefault();

    console.log('GET to Flask')
    this.dataService.getData(`home/${homeId}`).subscribe({
      next: (response: any) => {
        console.log('Response from backend:', response); // בדוק את התגובה
        if (response.message == 'Home not found'){
          alert(' לא ניתן לבחור');
        } else{
             // בדיקה אם התגובה היא אובייקט
          if (response && !Array.isArray(response)) {
            this.dataFrom = Object.values(response); // המרת אובייקט למערך
          } else {
            this.dataFrom = response; // במידה וזה כבר מערך
          }
        }

        this.dataError = response.message;
      },
      error: (error: any) => {
        console.error('Error:', error);

      }
    })
  }
}
