Title: Persistent Search Filtering with ASP.NET MVC Value Providers
Date: 2015-03-11 16:20
Tags: dotnet, aspnet, mvc
Slug: persistent-search-filtering-with-aspnet-mvc
Author: Matthew Rich
Summary: Want your MVC web app to remember your users' search parameters?  There's a feature for that.

One of the systems I maintain at my work is a large ASP.NET MVC5 web app for
handling applications for our summer, weekend, and online courses for gifted
K-12 students. We have records for hundreds of thousands of students from the
last 15 or so years, some with dozens of courses they have taken with us, and
presenting the staff with all the information they need to process the
applications is a challenge.

One problem we faced in particular was that, due to the way the list/detail
views were originally built (using an Ajax search/list interface and jQuery UI
modals for detail views) the app would forget a user's search parameters once
they clicked to an edit view or a different controller altogether. I knew that
the fix for this was to remember the user's search fields in the session but it
took me some time to come up with a technique that fits the framework; namely
the `IValueProvider` interface.

The feature is largely implemented via three classes: an attribute that can
decorate ViewModel properties that should be persisted in the session, a
session "helper" class that can take a ViewModel class and persist the right
properties in the session, and a value provider class that can populate a
ViewModel instances with values from the session.

### The Filter
Let's look first at the attribute, `PersistInSessionAttribute`:

	namespace MyWebApp.Util
	{
			public class PersistInSessionAttribute : Attribute
			{
			}
	}

This attribute as you can see does nothing at all, it's simply a name we can
use to later find the properties that we want to remember in the session.

We could of course not use this attribute and have our helper remember *every*
property of the ViewModel, but there will be things like `IQueryable<T>`
instances and lists of select options that we don't need to remember: all we
care about are the user's actual search parameters.

### The Session Helper
Now we need a way to remember the values of properties for a given ViewModel in
the session. For this I use a `SessionHelper` class which receives a wrapper
around the actual `HttpSessionStateBase` instance (for testing purposes) and
provides `Remember` and `Forget` methods:

#### SessionHelper.cs
	using MyWebApp.Util;

	namespace MyWebApp.Helpers
	{
			public class SessionHelper
			{
					private ISessionWrapper sessionWrapper;
					
					public SessionHelper(ISessionWrapper sessionWrapper)
					{
							this.sessionWrapper = sessionWrapper;
					}

					public void Remember(object model)
					{
							foreach (var prop in model.GetType().GetProperties())
							{
									var persistAttr = prop.GetCustomAttribute(typeof(PersistInSessionAttribute));
									if (persistAttr != null)
									{ 
											sessionWrapper.SetSessionValue(prop.Name, prop.GetValue(model, null));
									}
							}
					}

					public void Forget(Type modelType)
					{
							foreach (var prop in modelType.GetProperties())
							{
									var persistAttr = prop.GetCustomAttribute(typeof(PersistInSessionAttribute));
									if (persistAttr != null)
									{
											sessionWrapper.DeleteSessionValue(prop.Name);
									}
							}
					}
			}
	}

Note that both methods iterate over all properties of the passed-in object
looking for any decorated with the `PersistInSessionAttribute` and then either
set or delete the value for that property in the session.

Bonus `ISessionWrapper` interface and implementation!

#### ISessionWrapper.cs
	namespace MyWebApp.Util
	{
			public interface ISessionWrapper
			{
					object GetSessionValue(string key);
					void SetSessionValue(string key, object value);
					void DeleteSessionValue(string key);
					bool ContainsValue(string key);
			}
	}

#### HttpContextSessionWrapper.cs
	namespace MyWebApp.Util
	{
			public class HttpContextSessionWrapper : ISessionWrapper
			{
					private HttpSessionStateBase sessionState;

					public HttpContextSessionWrapper(HttpSessionStateBase sessionState)
					{
							this.sessionState = sessionState;
					}

					public object GetSessionValue(string key)
					{
							if (sessionState == null)
							{
									return null;
							}
							return sessionState[key];
					}

					public void SetSessionValue(string key, object value)
					{
							if (sessionState == null)
							{
									return;
							}
							sessionState[key] = value;
					}

					public bool ContainsValue(string key)
					{
							if (sessionState == null)
							{
									return false;
							}
							return sessionState[key] != null;
					}

					public void DeleteSessionValue(string key)
					{
							if (sessionState == null)
							{
									return;
							}
							sessionState.Remove(key);
					}
			}
	}

Not much to see there, just a thin shim to give us a place to swap out the
actual `HttpSessionStateBase` instance in an MVC controller for an alternate
implementation for testing purposes.

### The Value Provider
Here is where the magic happens. Once we register this value provider with the
framework, anytime a controller calls `UpdateModel` or `TryUpdateModel`, our
value provider will be called.

#### SessionSearchValueProvider.cs
	namespace MyWebApp.Util
	{
			public class SessionSearchValueProvider : IValueProvider
			{
					private ISessionWrapper session;
					
					public SessionSearchValueProvider(ISessionWrapper session)
					{
							this.session = session;
					}
					
					public bool ContainsPrefix(string prefix)
					{
							return session.ContainsValue(prefix);
					}

					public ValueProviderResult GetValue(string key)
					{
							object value = session.GetSessionValue(key);
							if (value == null)
							{
									return null;
							}
							return new ValueProviderResult(value, value.ToString(), CultureInfo.CurrentCulture);
					}
			}
	}

As you can see all this does is look at whatever `ISessionWrapper` instance is
passed in to the constructor to get the remembered values.

Now just a few more items of glue code to wire everything up.

First, a value provider factory for our value provider:

#### SessionSearchValueProviderFactory.cs
	namespace MyWebApp.Util
	{
			public class SessionSearchValueProviderFactory : ValueProviderFactory
			{
					public override IValueProvider GetValueProvider(ControllerContext controllerContext)
					{
							ISessionWrapper sessionWrapper = new HttpContextSessionWrapper(controllerContext.HttpContext.Session);
							return new SessionSearchValueProvider(sessionWrapper);
					}
			}
	}

Then, register the value provider factory in Global.asax:

#### Global.asax.cs
	using MyWebApp.Util;

	namespace MyWebApp.Web
	{
			public class MvcApplication : System.Web.HttpApplication
			{
					// boilerplate code removed

					protected void Application_Start()
					{
							AreaRegistration.RegisterAllAreas();

							RegisterGlobalFilters(GlobalFilters.Filters);
							RegisterRoutes(RouteTable.Routes);

							ValueProviderFactories.Factories.Add(new SessionSearchValueProviderFactory());
					}
			}
	}

Now one more optional step: make a new base class for our app's controllers
that instantiates the `SessionHelper` once the session is actually available:

#### MyWebAppController.cs
	using MyWebApp.Util

	namespace MyWebApp.Web.Controllers
	{
			public class MyWebAppController : Controller
			{
					protected SessionHelper sessionHelper;

					protected override void OnActionExecuting(ActionExecutingContext filterContext)
					{
							sessionHelper = new SessionHelper(new HttpContextSessionWrapper(Session));
							base.OnActionExecuting(filterContext);
					}
			}
	}

An MVC controller's `Session` property is not actually available until right
before the controller's action method is run, so we need to override
`OnActionExecuting` to grab it and instantiate our `SessionHelper`. This step
of pulling out this method into a base class is of course optional, but if
you're going to use this functionality in more than one controller it's a good
idea I think so you avoid repeating code.

Now, *finally*, we're ready to actually use the feature!

#### StudentSearchViewModel.cs
	using MyWebApp.Util;

	namespace MyWebApp.Models.ViewModels
	{
			public class StudentSearchViewModel
			{
					public IQueryable<Student> Students { get; set; }

					[PersistInSession]
					public string FirstNameSearch { get; set; }

					[PersistInSession]
					public string LastNameSearch { get; set; }

					public bool IsSearch
					{
							get
							{
									return !string.IsNullOrWhiteSpace(FirstNameSearch) ||
											!string.IsNullOrWhiteSpace(LastNameSearch);
							}
					}
			}
	}

The `IsSearch` property is used in the view to determine whether or not to show
a link to the `ClearSearch` action method.

#### StudentController.cs
	using MyWebApp.Models.ViewModels;
	namespace MyWebApp.Web.Controllers
	{
			public class StudentController : MyWebAppController
			{
					private StudentManager studentManager;

					public StudentController(IRepository repository)
					{
							studentManager = new StudentManager(repository);
					}

					public ActionResult Index()
					{
							var viewModel = new StudentSearchViewModel();

							// this will update the view model with any search parameters saved in the session!
							UpdateModel(viewModel);

							viewModel.Students = studentManager.DoStudentSearch(viewModel);

							return View(vm);
					}

					// in our app this is an Ajax action method but it could be a normal action method as well.
					public ActionResult List(string FirstNameSearch, string LastNameSearch)
					{
							var viewModel = new StudentSearchViewModel();

							// this will update the view model from both the query string parameters
							// and the session, with the query string overriding the session.
							UpdateModel(vm);

							// this saves the newly updated viewmodel's values into the session!
							sessionHelper.Remember(vm);

							viewModel.Students = studentManager.DoStudentSearch(viewModel);

							return PartialView(vm);
					}

					// the List view can check the viewmodel's `IsSearch` property and if it's truthy,
					// display a link to this action method, which will "forget" the values stored in
					// the session for just that viewmodel and then redirect the user back to the
					// Index action method.
					public ActionResult ClearSearch()
					{
							sessionHelper.Forget(typeof(StudentSearchViewModel));
							return RedirectToAction("Index");
					}
			}
	}

There are certainly a few ways this feature could be improved. Notably,
viewmodels that share the same property names will overwrite each other's
persisted values. In practice however this isn't a problem for us, as the users
seem to like that their search can "follow" them across controllers. Any other
suggestions are welcome!

