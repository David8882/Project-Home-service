import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private apiUrl = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) {}
  /**
 * Get data by ID or fetch all data.
 */
  getData(endpoint: string):  Observable<any>{
    return this.http.get<any>(`${this.apiUrl}/${endpoint}`)
}
  /**
  * Post Data row
  */

  sendData(endpoint: string, data: any):  Observable<any>{
    return this.http.post<any>(`${this.apiUrl}/${endpoint}`, data)
}

  /**
  *Delete row
  */
  deletePost(endpoint: string, id: number):  Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${endpoint}/${id}`);
}


}
