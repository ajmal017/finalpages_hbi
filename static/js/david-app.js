

/*
			KEY COMPONENTS:
			"activeItem" = null until an edit button is clicked. Will contain object of item we are editing
			"list_snapshot" = Will contain previous state of list. Used for removing extra rows on list update

			PROCESS:
			1 - Fetch Data and build rows "buildList()"
			2 - Create Item on form submit
			3 - Edit Item click - Prefill form and change submit URL
			4 - Delete Item - Send item id to delete URL
			5 - Cross out completed task - Event handle updated item

			NOTES:
			-- Add event handlers to "edit", "delete", "title"
			-- Render with strike through items completed
			-- Remove extra data on re-render
			-- CSRF Token
		*/

function getCookie(name) {
		    var cookieValue = null;
		    if (document.cookie && document.cookie !== '') {
		        var cookies = document.cookie.split(';');
		        for (var i = 0; i < cookies.length; i++) {
		            var cookie = cookies[i].trim();
		            // Does this cookie string begin with the name we want?
		            if (cookie.substring(0, name.length + 1) === (name + '=')) {
		                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		                break;
		            }
		        }
		    }
		    return cookieValue;
		}
		var csrftoken = getCookie('csrftoken');

		var activeItem = null
		var list_snapshot = []


buildList()

		// This function is responsible for fetching data from back-end and output data into the document
		function buildList(){
			var wrapper = document.getElementById('list-wrapper')
			//wrapper.innerHTML = ''

			//fetching data from backend
			//var url = 'http://127.0.0.1:8000/api/task-list/'
			var url = 'http://127.0.0.1:8000/mydocuments/task-list/'
			var urledit = 'http://127.0.0.1:8000/mydocuments/edit/'

			fetch(url)
			.then((resp) => resp.json())
			.then(function(data){
				console.log('Data:', data)  //display at console
            // render the data into the document
				var list = data
				for (var i in list){

          // check for exceptions
					try{
						document.getElementById(`data-row-${i}`).remove()
					}catch(err){

					}


          // render title

					var title = `<span class="title">${list[i].title}</span>`
                    var check01

                    /*
                    if (list[i].is_published == true){
						title = `<strike class="title">${list[i].title}</strike>`
					}*/

					if (list[i].is_published == true){
						check01 = `<input type="checkbox" name="{{ item.id }}" id="{{ item.id }}" checked><span><label for="{{ item.id }}"></label></span>`
                    }
                    else{
                        check01 = `<input type="checkbox" name="{{ item.id }}" id="{{ item.id }}"><span><label for="{{ item.id }}"></label></span>`
                    }

                    // console.log('item =',i,list[i].is_published);

					// render individual items
					var item = `
						<div id="data-row-${i}" class="task-wrapper flex-wrapper">

                            <!-- display title -->
							<div style="flex:7">${title}</div>

                            <!-- display title -->
							<div style="flex:3">
							    <div class="switch-button switch-button-xs">
							        ${check01}
                                 </div>
							</div>

							<div style="flex:2">
							    <a href="${urledit}${list[i].id}" class="badge badge-pill badge-success">Edit</a>
								<!-- <button class="btn btn-sm btn-outline-info edit">Edit</button>  -->
							</div>

							<div style="flex:1">
								<button class="btn btn-sm btn-outline-dark delete">Delete</button>
							</div>

						</div>



					`
					wrapper.innerHTML += item



				}


//******************************************************************************************************

if (list_snapshot.length > list.length){
					for (var i = list.length; i < list_snapshot.length; i++){
						document.getElementById(`data-row-${i}`).remove()
					}
				}

				list_snapshot = list


				for (var i in list){
					var deleteBtn = document.getElementsByClassName('delete')[i]
					var title = document.getElementsByClassName('title')[i]

					deleteBtn.addEventListener('click', (function(item){
						return function(){
							deleteItem(item)
						}
					})(list[i]))

				}

//********************************************************************************************************

function deleteItem(item){
			console.log('Delete clicked item =', list[i].id)

			fetch(`http://127.0.0.1:8000/mydocuments/task-delete/${item.id}/`,
			{
				method:'DELETE',
				headers:{
					'Content-type':'application/json',
					'X-CSRFToken':csrftoken,
				}
			}).then((response) => {
				buildList()
			})
		}




})
}