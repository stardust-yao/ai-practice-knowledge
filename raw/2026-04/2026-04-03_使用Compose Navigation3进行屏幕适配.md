---
title: 使用Compose Navigation3进行屏幕适配
date: 2026-04-03
source: https://mp.weixin.qq.com/s?__biz=Mzg3Njc0NTgwMg==&amp;mid=2247504142&amp;idx=1&amp;sn=305433f230b634c8b3d3215cd4b962d1
account: 哔哩哔哩技术
fetched_at: 2026-07-31 12:38:25 CST
article_id: 305433f230b634c8b3d3215cd4b962d1
---

原创 大前端 2026-04-03 12:02 上海

  
  
*[图片]*

  
  
这篇文章将介绍B站是怎么使用 Compose Navigation3 进行页面的宽屏适配，并解决其中遇到的问题的。

本文所涉及到的 Compose 页面均已完成了 CMP 跨平台化适配，内容中基于安卓习惯所提的 “Activity” 如无额外说明均代表各平台的页面容器，即可以直接替换为iOS的UIViewController理解。

**Navigation3 简介**

Navigation3 是 Google 在 2025 年推出的全新 Compose 导航库，与之前的 Navigation Compose 有本质区别。它不再内置导航图（NavGraph）和 NavHost，而是将导航栈的管理权完全交给开发者，框架只负责"根据栈内容渲染 UI"，将 f(data)=UI 的理念扩展到了页面导航栈上。得益于这新的精简的框架概念，使得 Navigation3 能很轻松地跟现有大型app的路由系统搭配整合使用，不像之前的 Navigation 库那样需要将现有路由完全迁移到导航图（NavGraph）声明上。开发者完全可以在单模块内进行 Nav3 的接入使用，同时保持整体的路由声明方式。

虽然使用Compose编写的页面，因其声明式的特性，已经有良好的响应屏幕宽度变化的能力。但是近期出现的超宽、折叠屏手机，包括鸿蒙平台的平板、桌面等设备，会让仅支持响应式布局的页面在超宽显示模式下给用户带来不好的视觉和交互体验。与Navigation3 库同时提出的“WindowSizeClass”中，将屏幕根据宽度划分为小、中、大等各个档位。这种“断点式”的屏幕划分可以指导我们知道在怎么样的情况下将应用的界面显示编排成全屏页面还是分屏页面的形式，显著提高在折叠屏、平板、桌面等“非传统手机”屏幕下的用户呈现能力。

**为什么需要纯Compose的导航框架**

在b站深入推进业务 CMP 跨平台化的过程中，我们发现缺少一个适配 CMP 属性的页面导航框架是深入业务使用的一大阻碍。

在先前的页面方案中，我们仿照安卓原生实现，选择了为每个导航节点嵌套一个原生window容器，即每打开一个个 Composable 页面都对应一个安卓 Activity 、iOS UIViewController 和 鸿蒙 entry 的创建与展现。这个方案能让我们快速地将 Compose 页面集成到现有工程中，但随后带来了更多其他的问题。

首要面临的问题是内存压力。在 iOS 和鸿蒙中，每打开一个新的原生容器来承载Compose页面，都意味着一个 CAMetalLayer/NativeWindow 被创建，对应3倍大小的render buffer也会被创建在内存中，内存占用就会相应提升。根据我们测算，使用三缓冲区渲染的 iOS，每一个 CAMetalLayer 都会占用约40M的内存。随着接入Compose的页面越来越多、用户打开的页面越来越多，内存压力会不断增长，影响我们的CMP推进进程。

另一个问题是，Compose 上下文内使用的 Lifecycle 系统是基于安卓生命周期概念设计的，在 iOS 和鸿蒙系统中多少有些水土不服，需要 ComposeView 的宿主层进行额外的配置工作，例如将 UIViewController 的 willAppear didAppear等回调桥接到 androidx 生命周期的相应事件上。在“标准容器”无法满足页面展现需求，需要做业务定制的时候，这些额外配置将成为开发过程的摩擦，在接入者不熟悉/没有意识到需要做这些配置的时候，将严重拖慢review和交付进度。

并且，这样的桥接总会丢失准确信息，特别是在页面切换的时候，总会错过准确的生命周期回调，导致在后台执行了额外的工作，引起卡顿、发热等问题；

同时，不正确的生命周期事件会让开发有不正确的预期，这一点会在本文后面详细描述。

基于以上问题的考量，我们得出结论，至少在纯Compose世界内的页面导航切换范围内，我们需要一个纯Compose的导航框架。而刚刚推出正式版、其结构思想契合现代代码开发思路的Navigation3成为我们的首选方案。

**路由与导航的区别和联系**

在之前的开发理念中，我们往往将"路由"和"导航"混为一谈：一个 URI 既是页面的标识，也是跳转的触发方式。我们将URI标注在一个 Fragment/Activity 上之后，调用“路由”跳转这个URI将直接打开这个页面实例。

```
@Route("bilibili://some/page")**`class SomePageActivity: Activity()````Router.routeTo("bilibili://some/page") // == startActivity(SomePageActivity.class)```然而，在后续的开发和迭代过程中，我们逐渐意识到，这一次跳转动作应当分为两个具体步骤：使用“路由”寻找这个 URI 对应的页面信息，然后使用“导航”组件将这个页面展现在用户面前。在我们的项目 CMP 化推进过程中，基架团队已经将这个理念应用到了b站的 CMP 版路由组件中，允许业务方在复用公共路由表的查找逻辑和结果的前提下，根据不同页面需要自定义自己的“路由结果导航”行为，为这次的 Nav3 快速接入提供了合适切入点。**数据驱动的声明式导航栈展现**Navigation3 的核心理念是：导航栈就是一个普通的 List，UI 是这个 list 的函数。
```
`class MyBackStackK : NavKey>(private val list: SnapshotStateList) : SnapshotStateList by list {``    override funadd(item: K){``        // 可以在这里提前处理冲突元素的清理``        list.add(item)``    }``}````@Composable``funNavPage(modifier: Modifier = Modifier){``    val backStack = remember {``        mutableStateListOf(HomeNavKey)``    }````    NavDisplay(``        backStack = backStack,           // 数据：当前栈内容``        sceneStrategy = ...,             // 策略：如何将栈内容映射为布局``        entryDecorators = listOf(...),   // 装饰器：为每个 entry 注入能力``        entryProvider = entryProvider {   // 注册：NavKey → Composable 的映射``            entry { key -> SomePage(key) }``        },``    )``}`
```
开发者只需要按照自己的页面逻辑操作 backStack ，例如添加、移除，或者“在特定页面入栈时清除其他页面”用来实现“最多只有一个详情页被打开”的情况。NavDisplay 会自动响应变化并重新计算布局。不需要手动调用 navigate()、popBackStack() 等命令式 API，更加贴合 Compose 生态中的开发习惯。**在实际业务中接入使用**在实际的业务场景中使用 Navigation3 ，当然不像其他网络示例那样简单调用。我们将需要深入使用 Nav3 库提供的各种 api ，定制自己的业务功能。**NavKey 与路由发现**在 Nav3 中，NavKey 是描述页面的最小独立元素，每一个 NavKey 类型都跟一个页面绑定，描述了期望被打开的页面的基础信息，例如请求这个页面所需的唯一ID：
```
`@Serializable``@Route("bilibili://some/nav3/page/with/id/{id}")``data class SomeIdPageNavKey(``    val id: String,``    val paramFromQuery: String,``) : NavKey````@Route("bilibili://some/page/with/id/{id}")``@Composable``funSomePage(id: String, modifier: Modifier = Modifier, paramFromQuery: String = ""){}`
```
因为一个 NavKey 可以跟一个路由严格对应，所以以上这段声明代码完全可以交给路由的 KSP 处理器自动生成。在子页面发起正常的路由跳转请求时，通过拦截器模式拦截此次路由的查找过程，如果找到匹配的 NavKey 类型，则将一个实例添加到backStack栈顶，将普通的导航行为桥接到 Nav3 的导航中。
```
`// 路由拦截器：将普通路由请求桥接到 Nav3 的 backStack``class Nav3RouteInterceptorKEY : NavKey>(``    private val onNavKeyFound: (KEY) -> Boolean,``) : Interceptor {``    override funintercept(chain: Interceptor.Chain): Response {``        val originUri = chain.uri``        // 将原始 URI 转换为 Nav3 专用的查找格式``        // 例如 bilibili://some/page/123 → bilibili://some/nav3/page/123``        val navUri = convertToNav3Uri(originUri) ?: return chain.proceed()````        // 在路由表中查找这个 URI 对应的 NavKey 工厂函数``        val target = chain.find(navUri) as? SomeIdPageNavKey````        returnif (key != null && onNavKeyFound(key)) {``            Response.Done  // 拦截成功，阻止后续的默认导航行为（如 startActivity）``        } else {``            chain.proceed() // 未匹配，交给下一个拦截器或默认处理``        }``    }``}````// 在 Nav3 宿主页面中组装拦截器``@Composable``funNav3HostPage() {``    val backStack = remember { mutableStateListOf(HomeNavKey) }````    // 创建拦截器，拦截成功时将 NavKey 推入栈``    val interceptor = remember {``        Nav3RouteInterceptor { key ->``            backStack.add(key)``        }``    }``    // 在原有 Router 上叠加拦截器，生成新的 Router 实例``    val localRouter = LocalRouter.current``    val nav3Router = remember(localRouter, interceptor) {``        localRouter.newBuilder().addInterceptor(interceptor).build()``    }````    NavDisplay(``        backStack = backStack,``        entryDecorators = listOf(``            // 通过 Decorator 将带拦截器的 Router 注入到所有子页面``            // 这样子页面内发起的路由请求也会经过拦截器``            remember { Nav3RouterDecorator(nav3Router) },``            ...``        ),``        ...``    )``}````// Decorator 实现：通过 CompositionLocal 注入 Router``class Nav3RouterDecorator(``    private val router: Router,``) : NavEntryDecorator(``    onPop = {},``    decorate = { entry ->``        CompositionLocalProvider(LocalRouter provides router) {``            entry.Content()``        }``    },``)`
```
NavKey 需要支持序列化（用于 backStack 的保存/恢复），因此都标注了 @Serializable；当然，也可以选择统一保存原始跳转链接的string内容，在需要恢复时重新走一次路由查找。**NavKey 与 entry 注册**NavKey 仅能表示“有一个页面”，在 Nav3 中，还需要通过 entryProvider 的方式将“这个 NavKey 对应的页面如何显示” 注册到当前的 NavDisplay 中：
```
`NavDisplay(``    backStack = backStack,``    entryProvider = entryProvider {``        entrySomeIdPageNavKey>(metadata = BiliListDetailSceneStrategy.detailPane()) { key -> SomePage(key.id, Modifier, key.paramFromQuery) }``    },`` )`
```
当然，这一段注册代码也可以抽象为 EntryProviderScope.() -> Unit 的函数，由路由 KSP 处理器统一生成，页面只需要按需注册即可。**SceneStrategy 与 Scene**SceneStrategy 是 Navigation3 中最关键的扩展点。它接收当前 backStack 中所有 entry，返回一个 Scene 来描述如何布局。在我们的宽屏适配实践中，我们实现了 BiliDetailSceneStrategy：
```
`class BiliDetailSceneStrategyK : NavKey>(``    val windowSizeClass: WindowSizeClass,``) : SceneStrategy {``    override fun SceneStrategyScope.calculateScene(entries: ListNavEntryK>>): Scene? {``        if (windowSizeClass.isAtLeastMedium(...)) {``            // 宽屏：从栈中找到最后一个 List entry 和最后一个 Detail entry``            val listEntry = entries.findLast { it.metadata.containsKey(LIST_KEY) }``                ?: return null``            val detailEntry = entries.findLast {``                it.metadata.containsKey(DETAIL_KEY)``            }``            return BiliListDetailScene(``                listEntry = listEntry,``                detailEntry = detailEntry,``                listWidth = if (windowSizeClass.widthLargeCompat()) 375.dp else300.dp,``            )``        }``        return null  // 非宽屏的情况：返回 null，表示当前 Strategy 不处理这个情况，NavDisplay 将使用默认单页 Strategy``    }``}`
```
BiliListDetailScene 的布局结构：
```
`Row(modifier = Modifier.fillMaxSize()) {``    // 左栏：列表``    Box(modifier = Modifier.width(listWidth)) {``        listEntry.Content()``    }``    VerticalDivider(...)``    // 右栏：详情或占位图``    Box(modifier = Modifier.weight(1f)) {``        if (detailEntry != null) {``            CompositionLocalProvider(LocalBackIconVisibility provides false) {``                detailEntry.Content()``            }``        } else {``            DefaultDetailPlaceholder()``        }``    }``}`
```
每个 entry 通过 metadata 标记自己属于哪个区域。metadata 在注册 entry 时通过 BiliListDetailSceneStrategy.listPane() / detailPane() 设置：
```
`companion object {``    funlistPane()= mapOf("BiliListDetailScene-List" to true)``    fundetailPane()= mapOf("BiliListDetailScene-Detail" to true)``}`
```
SceneStrategy 的 calculateScene 在每次 backStack 变化时都会被调用。如果设备发生折叠/展开，windowSizeClass 变化会触发 BiliListDetailSceneStrategy 的重建（通过 remember(windowSizeClass)），从而自动切换单栏/双栏布局。**踩过的一些坑**从原生导航模式迁移到 Nav3 ，页面的导航方式将发生重大变化，其中有不少在往常开发过程中注意不到的地方。**生命周期、页面重入、状态保存**首先最大的一个变化，是之前每一次导航到一个 Composable 函数页面，都将打开一个全新的 Activity 来承载这个函数体，因此开发们会有一个错误认知：Compose Scope = Activity Scope = ViewModel Scope，在副作用处理上容易出现错误和遗漏，例如：
```
`// ViewModel 中，将 toast 信息作为 State 的一部分暴露``data class PageState(``    val items: List = emptyList(),``    val toast: ToastContent? = null,  // 一次性事件，混在持久状态中``)````class SomeViewModel : ViewModel(){``    val state: StateFlow = ...````    funonAction(action: Action) {``        // 某些操作会产生 toast``        _state.update { it.copy(toast = ToastContent("操作成功")) }``    }``}````@Composable``funSomePage(viewModel: SomeViewModel) {``    val state by viewModel.state.collectAsState()``    val toaster = LocalToaster.current````    var otherState = remember { mutableStateOf("") }````    // 通过 snapshotFlow 监听 state 变化来显示 toast``    LaunchedEffect(Unit) {``        snapshotFlow { state.toast }``            .filterNotNull()``            .distinctUntilChanged()``            .collect { toaster.showToast(it.content) }``    }````    // 或者直接判断内容进行显示，都会引发同样的问题。``    // LaunchedEffect(state.toast) {``    //    state.toast?.let { toaster.showToast(it.content) }``    // }````    // ... 页面内容``}`
```
在独立的 Activity 中，这段代码运行起来不会有问题；但是在 Navigation3 的单Activity导航栈模式下，从这个页面跳转到其他页面之后，这个页面将暂时“退出组合”，在返回这个页面之后，重新“进入组合”。在这个过程中，并不算一次“重组”，而是一次全新的组合事件，上面的代码将会出现：1.  不管 LaunchedEffect 的key是什么，都会进入一次执行，snapshotFlow中记录的前值也将被清空，导致 toast 被重复显示；2.  通过 remember 保存的状态也被清空，依赖 remember 做的逻辑将回到空态。针对以上问题，修复思路其实很简单。对于第一个问题，首先需要开发者确认什么内容该属于“状态”，什么内容该属于“事件”。在示例代码中，val items: List 属于需要在页面上一直显示的内容，属于业务状态的一部分，使用 StateFlow 和 collectAsState 是很恰当的；而对于 toast 来说，已经显示过一次的toast内容在任何情况下都不该重新出现，因此它该属于“事件流”的一部分，每次消费后都不再重放，因此可以使用 sharedFlow 承载toast的传递，或者每次显示完主动将这个字段清空。而第二个问题则更简单了，首先区分被 remember 的数据是否能接受丢失，如果是可以丢失的状态（例如，播放中的动画进度）则完全可以不处理；对于真正需要保存的数据，可以通过实现自定义 Saver 使用 rememberSavable 的方式，或者将数据委托给 ViewModel 中保存。
```
`data class PageState(``    val items: List = emptyList(),``    val toast: ToastContent? = null,``)````class SomeViewModel : ViewModel(){``    private val _state = MutableStateFlow(PageState())``    val state: StateFlow = _state.asStateFlow()````    // 将 state 中的 toast 字段转换为事件流（replay=0，重新订阅不重放历史事件）``    val toastEvent: SharedFlow = state``        .map { it.toast }``        .filterNotNull()``        .shareIn(viewModelScope, SharingStarted.Eagerly, replay = 0)````    funonAction(action: Action) {``        _state.update { it.copy(toast = ToastContent("操作成功")) }``        // 也可以选择显示后立即清空，确保 toast 状态不会被持久持有``        // _state.update { it.copy(toast = null) }``    }``}````@Composable``funSomePage(viewModel: SomeViewModel) {``    val state by viewModel.state.collectAsState()``    val toaster = LocalToaster.current````    // 需要跨页面跳转保留的状态，改用 rememberSaveable``    var otherState by rememberSaveable { mutableStateOf("") }````    // 消费事件流：重新进入组合时重新订阅，replay=0 保证不会重放已消费的事件``    LaunchedEffect(Unit) {``        viewModel.toastEvent.collect { toast ->``            toaster.showToast(toast.content)``        }``    }````    // ... 页面内容``}`
```
Navigation3使用额外依赖中的 rememberViewModelStoreNavEntryDecorator() 来提供“页面在pop时清空相应viewmodel”的能力。并且在未来这个依赖和ViewModelStore的能力和api将会发生变化，带来更加强大的定制能力。屏幕状态感知与返回按钮**

宽屏模式下，右栏的页面不需要显示返回按钮（因为左栏始终可见）。可以通过自定义 LocalBackIconVisibility 这个 CompositionLocal 控制：

```
`val LocalBackIconVisibility = compositionLocalOf { true }`**```// 右栏渲染``if (detailEntry != null) {``    CompositionLocalProvider(LocalBackIconVisibility provides false) {``        detailEntry.Content()``    }``}`
```
子页面中通过读取这个值来决定是否显示返回图标：
```
`val showBackButton = LocalBackIconVisibility.current
```
窄屏模式下 LocalBackIconVisibility 保持默认值 true，页面正常显示返回按钮。**状态栏的控制**在单 Activity 页面导航框架中， SystemUI 配置（如状态栏颜色）如果允许每个页面、每个组件自由控制，将很容易出现UI闪烁等情况。我们通过 SystemUiConfiguration 收集机制解决：每个 entry 通过 collectSystemUiConfiguration Modifier 上报自己的配置，NavDisplay所在的宿主页面 取栈顶 entry 的配置应用到宿主：// ① 定义：持有状态栏配置的可观察容器``@Stable``class StableSystemUiConfiguration {``    var statusBarDarkIcons: Boolean? by mutableStateOf(null)``}````// ② 宿主：为每个 NavKey 分配一个 config 对象，并将"锚点 modifier"传给 entry``val configurationMap = remember { mutableStateMapOf() }``val topConfiguration by remember {``    derivedStateOf { backStack.lastOrNull()?.let { configurationMap[it] } }``}````val getCollectorModifier: (MyNavKey) -> Modifier = { key ->``    val config = configurationMap.getOrPut(key) { StableSystemUiConfiguration() }``    // collectSystemUiConfiguration 在 modifier 链中埋入"锚点"，持有 config 的引用``    Modifier.collectSystemUiConfiguration(config)``}````NavDisplay(``    // 将栈顶 entry 的配置应用到 Window（状态栏颜色等）``    modifier = Modifier.applySystemUiConfiguration(topConfiguration),``    entryProvider = entryProvider {``        // 在构建 entryProvider 时将 collector modifier 传入页面``        entry { key ->``            SomePage(modifier = getCollectorModifier(key))``        }``    },``    ...``)````// ③ 子页面：将自己期望的状态栏配置追加到 modifier 链上``@Composable``funSomePage(modifier: Modifier = Modifier) {``    val isDarkTheme = LocalDarkTheme.current``    Box(``        // statusBarDarkIcons 会沿 modifier 链向上查找"锚点"，找到后将值写入宿主的 config 对象``        // 节点 attach 时写入，detach 时自动清空，生命周期安全``        modifier = modifier.statusBarDarkIcons(darkIcons = !isDarkTheme)``    ) {``        // 页面内容``    }``}`
```
而 NavDisplay 本身所在的页面中，框架已经传入了一个collectSystemUiConfiguration，并且将实际在 window 中生效。通过显式传递控制链条的方式，我们将状态栏的配置权限限制在页面宿主层级，在这一层让业务根据自己的实际逻辑决定内部组件的生效范围。**返回事件的处理**与 Navigation3 库同时推出的，是 androidx.navigationevent 库，用来响应和发送页面导航事件。Nav3 库默认已经使用了这个依赖库来响应返回事件，其行为是将现有的 backStack 的最新一个元素推出。如果我们需要定制返回事件的处理，可以通过包装 backStack 实现。需要注意的是，androidx.navigationevent 库会将系统返回手势、系统导航栏返回键、应用顶部导航栏返回按钮或其他主动调用 backHandler.backCompleted() 处的返回事件一同给出，现有的注册层级结构关系不能区分出返回事件的来源行为和来源页面。因此，暂时无法实现“分栏页面各有一个返回按钮，各自控制其栏位的页面pop”交互。**原生页面嵌入**在需要进行宽屏适配的模块中，部分页面仍然是 Android Fragment 实现，尚未迁移到 CMP。我们选择通过 BiliNativePage 将 Fragment 嵌入 Navigation3 体系：
```
`@Composable``internal funBiliNativePage(url: String, modifier: Modifier){``    val showBackButton = LocalBackIconVisibility.current``    // 1. 通过 Router 解析 URL，获取 Fragment Class``    val routeInfo = Router.newCall(url).find()``    val clazz = routeInfo?.clazz````    // 2. 使用 AndroidFragment 嵌入 Compose``    if (clazz != null) {``        // 3. 因为 AndroidFragment 尚不支持响应state变化主动更新参数，因此选择一个key主动进行重组，通过切换fragment的方式将新的 showBackButton 传入``        // 也可以选择使用 ViewModel 传递 showBackButton 的更新，避免fragment的重建``        key(showBackButton) {``            AndroidFragment(``                clazz = clazz as Classout Fragment>,``                modifier = modifier,``                arguments = createRouteExtraForFragment(routeInfo).also {``                    it.putBoolean("show_back_button", showBackButton)``                },``            )``        }``    }``}````// Fragment 侧：从 arguments 读取 show_back_button 控制返回按钮显隐``class SomePageFragment : Fragment(R.layout.fragment_some_page) {``    private val showBackButton get() = arguments?.getBoolean("show_back_button", true) ?: true````    override funonViewCreated(view: View, savedInstanceState: Bundle?) {``        super.onViewCreated(view, savedInstanceState)``        binding.btnBack.isVisible = showBackButton``        binding.btnBack.setOnClickListener { parentFragmentManager.popBackStack() }``    }``}`
```
原生页面的注册可以通过 expect/actual 机制来声明，或者使用依赖注入框架来实现页面注册。showBackButton 的变化会触发 Fragment 重建（通过 key(showBackButton)），确保 Fragment 能响应宽屏/窄屏切换时返回按钮的显隐变化。**Scene 中的小发现**在尝试在Nav3框架内添加页面切换动画过程中，我调研了官方示例 nav3-recipes 中关于动画切换的部分，结果看到了一段让我始料未及的代码：
```
`override val content: @Composable (() -> Unit) = {``    Row(modifier = Modifier.fillMaxSize()) {``        Column(modifier = Modifier.weight(0.4f)) {``            listEntry.Content()``        }``        ...````        Column(modifier = Modifier.weight(0.6f)) {``            AnimatedContent(``                ...``            ) { entry ->``                entry.Content()``            }``         }``     }``}`
```
其中的 entry.Content() 让我产生了“这能正常触发重组吗？”的疑问🤔。在通常的开发惯例中，Composable 函数一般都是独立于Kotlin class的顶层函数，而不是某个实例的成员函数来被调用，这样 Compose 框架可以通过分析入参是否变化来决定是否重组；如果函数本身是一个类对象的成员函数，那类实例的改变会不会产生类似于key改变的作用、从而触发了这个Composable函数的完全重组呢？带着这个疑问，我构造了一段测试代码：
```
`@Immutable``data class TestClass(val data: String){``    @Composable funContent(modifier: Modifier = Modifier){``        Text(data)``    }``}`
```
然后使用 jadx 查看它编译后的产物，看到了关键信息：
```
`public final classTestClass{``    public static final int $stable = 0;``    private final String data;``    /* JADX INFO: Access modifiers changed from: private */``    public static final Unit Content$lambda$0(TestClass testClass, Modifier modifier, int i, int i2, Composer composer, int i3) {``        testClass.Content(modifier, composer, RecomposeScopeImplKt.updateChangedFlags(i | 1), i2);``        return Unit.INSTANCE;``    }``    public TestClass(String data){``        Intrinsics.checkNotNullParameter(data, "data");``        this.data = data;``    }``    public final String getData(){``        returnthis.data;``    }``    public final void Content(Modifier modifier, Composer $composer, finalint $changed, finalint i){``        Composer $composer2;``        final Modifier modifier2;``        Composer $composer3 = $composer.startRestartGroup(507862195);``        ComposerKt.sourceInformation($composer3, "C(Content)N(modifier)160@6025L10:ListDetailScene.kt#qpkuy4");``        int $dirty = $changed;``        if(($changed & 48) == 0) {``            $dirty |= $composer3.changed(this) ? 32 : 16;``        }``        if(!$composer3.shouldExecute(($dirty & 17) != 16, $dirty & 1)) {``            $composer2 = $composer3;``            $composer2.skipToGroupEnd();``            modifier2 = modifier;``        } else {``            Modifier modifier3 = (i & 1) != 0 ? Modifier.INSTANCE : modifier;``            if(ComposerKt.isTraceInProgress()) {``                ComposerKt.traceEventStart(507862195, $dirty, -1, "com.example.nav3recipes.scenes.listdetail.TestClass.Content (ListDetailScene.kt:159)");``            }``            $composer2 = $composer3;``            TextKt.m4145TextNvy7gAk(this.data, null, 0L, null, 0L, null, null, null, 0L, null, null, 0L, 0, false, 0, 0, null, null, $composer2, 0, 0, 262142);``            if(ComposerKt.isTraceInProgress()) {``                ComposerKt.traceEventEnd();``            }``            modifier2 = modifier3;``        }``        ScopeUpdateScope scopeUpdateScopeEndRestartGroup = $composer2.endRestartGroup();``        if(scopeUpdateScopeEndRestartGroup != null) {``            scopeUpdateScopeEndRestartGroup.updateScope(new Function2() { // from class: com.example.nav3recipes.scenes.listdetail.TestClass$$ExternalSyntheticLambda0``                @Override // kotlin.jvm.functions.Function2``                publicfinal Object invoke(Object obj, Object obj2) {``                    return TestClass.Content$lambda$0(this.f$0, modifier2, $changed, i, (Composer) obj, ((Integer) obj2).intValue());``                }``            });``        }``    }``}`
```
会发现，这样一种成员Composable函数的产物跟顶层函数没什么区别，都是使用一个生成的数字key作为restart group的标记，在其中判断参数是否变化时，额外进行了 this 对象的判断，也就是说，可以简单将这个函数定义等价为：
```
`data class TestClass(val data: String)````@Composable``funContent($this: TestClass, modifier: Modifier = Modifier)`
```
基于这一层理解，就能确认，在nav3-recipes示例工程中，scene发生实例变化的时候，也等价于一个普通的Compose重组，其中可以依靠普通的重组、跳过和remember实现动画播放了。总结**

Navigation3 库的出现，极大地减轻了现有 app 在既存路由框架中接入使用的负担，让我们能快速地将现有的 Compose 页面接入其中，完成宽屏适配；同时也推动开发者在编写 Compose 页面的时候更加深入地思考该如何去适配它的生命周期与状态保存，提示代码的交付质量。

-End-

作者丨肖志康

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=b7584639&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzg3Njc0NTgwMg%3D%3D%26mid%3D2247504142%26idx%3D1%26sn%3D305433f230b634c8b3d3215cd4b962d1)
